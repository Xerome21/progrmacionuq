import cv2
import os

# Verificar si el archivo existe
video_path = r"C:\Users\kkyto\Desktop\hrzone\opencv_proyect\cv_proyect_part_2\parkinglot_video.mp4"
if not os.path.exists(video_path):
    print(f"Error: El archivo '{video_path}' no existe.")
    exit()

# Crear el objeto VideoCapture correctamente
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

fgbg = cv2.createBackgroundSubtractorMOG2()

print("Procesando video. Presiona ESC para salir.")

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Fin del video o error al leer un frame.")
        break
    
    # Redimensionar el frame (no el objeto VideoCapture)
    resized_frame = cv2.resize(frame, (360, 640))
    
    frame_count += 1
    if frame_count == 1:
        print(f"Primer frame leído. Dimensiones: {resized_frame.shape}")
    
    # Aplicar el extractor de fondo al frame redimensionado
    fgmask = fgbg.apply(resized_frame)
    
    cv2.imshow('Original', resized_frame)
    cv2.imshow('Detección de Movimiento', fgmask)
    
    # Aumenta el tiempo de espera para asegurar que los frames se muestren
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        print("Salida por tecla ESC.")
        break

cap.release()
cv2.destroyAllWindows()
print("Programa finalizado.")