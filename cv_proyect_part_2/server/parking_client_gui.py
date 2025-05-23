from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image
import parking_client
from parking_client import sendQR  # <-- Agrega esta línea
import os
import io
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
import numpy as np

SERVER_URL = "http://192.168.1.63:9090"

class CameraThread(QThread):
    frame_signal = pyqtSignal(QImage)
    qr_result_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_running = True
        self.capture = None

    def run(self):
        self.capture = cv2.VideoCapture('http://192.168.1.72:8080/video')
        if not self.capture.isOpened():
            self.qr_result_signal.emit("No se pudo acceder a la cámara.")
            return

        while self.is_running:
            ret, frame = self.capture.read()
            if not ret:
                continue

            # Emitir frame para mostrar en la GUI
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.frame_signal.emit(qt_image)

            # Decodificar QR
            pil_img = Image.fromarray(rgb_frame)
            decoded_objs = decode(pil_img)
            if decoded_objs:
                qr_data = decoded_objs[0].data  # bytes
                qr_text = qr_data.decode('utf-8')
                result = sendQR(SERVER_URL, qr_text)
                self.qr_result_signal.emit(result)
                break

        if self.capture is not None:
            self.capture.release()

    @pyqtSlot()
    def stop_capture(self):
        self.is_running = False
        if self.capture is not None:
            self.capture.release()

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escanear QR")
        self.setFixedSize(640, 480)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_frame(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Client GUI")

        # Labels
        l1 = QLabel('ID:')
        l2 = QLabel('Contraseña:')
        l3 = QLabel('Programa:')
        l4 = QLabel('Rol:')

        # Inputs
        self.e1 = QLineEdit()
        self.e2 = QLineEdit()
        self.e2.setEchoMode(QLineEdit.Password)
        self.e3 = QLineEdit()
        self.role_combo = QComboBox()
        self.role_combo.addItems(["student", "professor", "administrative"])

        # Buttons
        b_register = QPushButton('Registrar Usuario')
        b_register.clicked.connect(self.register_user)
        b_qr = QPushButton('Obtener QR')
        b_qr.clicked.connect(self.request_qr)
        b_send = QPushButton('Enviar QR')
        b_send.clicked.connect(self.send_qr)

        # QR label
        self.qr_label = QLabel("El QR aparecerá aquí")
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setFixedSize(220, 220)

        # Layout
        grid = QGridLayout()
        grid.addWidget(l1, 0, 0)
        grid.addWidget(self.e1, 0, 1)
        grid.addWidget(l2, 1, 0)
        grid.addWidget(self.e2, 1, 1)
        grid.addWidget(l3, 2, 0)
        grid.addWidget(self.e3, 2, 1)
        grid.addWidget(l4, 3, 0)
        grid.addWidget(self.role_combo, 3, 1)
        grid.addWidget(b_register, 4, 0, 1, 2)
        grid.addWidget(b_qr, 5, 0, 1, 2)
        grid.addWidget(b_send, 6, 0, 1, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.qr_label)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

    def register_user(self):
        id = self.e1.text()
        password = self.e2.text()
        program = self.e3.text()
        role = self.role_combo.currentText()
        if not id or not password or not program or not role:
            QMessageBox.critical(self, "Error", "Todos los campos son obligatorios.")
            return
        response = parking_client.registerUser(SERVER_URL, id, password, program, role)
        QMessageBox.information(self, "Registro", response)

    def request_qr(self):
        id = self.e1.text()
        password = self.e2.text()
        if not id or not password:
            QMessageBox.critical(self, "Error", "ID y contraseña requeridos.")
            return
        imgBytes = parking_client.getQR(SERVER_URL, id, password)
        if not imgBytes:
            QMessageBox.critical(self, "Error", "Usuario no existe o contraseña incorrecta.")
            return

        qr_folder = r"C:\Users\kkyto\Desktop\qr_codes"
        os.makedirs(qr_folder, exist_ok=True)
        qr_filename = f"qr_code_{id}_{int(datetime.now().timestamp())}.png"
        save_path = os.path.join(qr_folder, qr_filename)

        image = Image.open(io.BytesIO(imgBytes))
        image.save(save_path)

        pixmap = QPixmap(save_path).scaled(200, 200, Qt.KeepAspectRatio)
        self.qr_label.setPixmap(pixmap)
        self.qr_label.setText("")
        QMessageBox.information(self, "QR Code", f"Código QR guardado en {save_path}")

    def send_qr(self):
        self.camera_window = CameraWindow()
        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.camera_window.update_frame)
        self.camera_thread.qr_result_signal.connect(self.show_qr_result)
        self.camera_window.show()
        self.camera_thread.start()

    def show_qr_result(self, result):
        self.camera_window.close()
        QMessageBox.information(self, "Código QR escaneado", result)
        self.camera_thread.is_running = False

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec()