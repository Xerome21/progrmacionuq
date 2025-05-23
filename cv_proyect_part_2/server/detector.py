import cv2
import numpy as np
import imutils
import json  # Al inicio del archivo

cap = cv2.VideoCapture('http://192.168.1.72:8080/video')

# Historial y promedios por área
contour_history = [[] for _ in range(10)]
avg_contours = [0] * 10
frame_count = 0
initialized = False

# Variables independientes por área (coinciden con available_spots)
A1 = A2 = A3 = A4 = A5 = B1 = B2 = B3 = C1 = C2 = False

def scale_polygon(polygon, scale=1):
    centroid = np.mean(polygon, axis=0)
    return ((polygon - centroid) * scale + centroid).astype(int)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=360)

    # Definir áreas para cada lugar (ajusta las coordenadas según tu imagen)
    areaA1 = scale_polygon(np.array([[300, 20], [340, 20], [340, 90], [300, 90]]))
    areaA2 = scale_polygon(np.array([[250, 20], [290, 20], [290, 90], [250, 90]]))
    areaA3 = scale_polygon(np.array([[200, 20], [240, 20], [240, 90], [200, 90]]))
    areaA4 = scale_polygon(np.array([[145, 20], [185, 20], [185, 90], [145, 90]]))
    areaA5 = scale_polygon(np.array([[90, 20], [130, 20], [130, 90], [90, 90]]))
    areaB1 = scale_polygon(np.array([[305, 180], [340, 180], [340, 250], [305, 250]]))
    areaB2 = scale_polygon(np.array([[255, 180], [295, 180], [295, 250], [255, 250]]))
    areaB3 = scale_polygon(np.array([[205, 180], [245, 180], [245, 250], [205, 250]]))
    areaC1 = scale_polygon(np.array([[145, 180], [185, 180], [185, 250], [145, 250]]))
    areaC2 = scale_polygon(np.array([[90, 180], [130, 180], [130, 250], [90, 250]]))
    areas = [areaA1, areaA2, areaA3, areaA4, areaA5, areaB1, areaB2, areaB3, areaC1, areaC2]

    # Crear máscaras
    masks = []
    for area in areas:
        mask = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
        mask = cv2.drawContours(mask, [area], -1, (255), -1)
        masks.append(mask)

    # Procesar cada área
    canny_results = []
    contour_counts = []
    for mask in masks:
        area_img = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(area_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blur, 75, 100)
        canny_results.append(canny)

    # Contar contornos por área
    for idx, canny in enumerate(canny_results):
        cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_counts.append(len(cnts))
        for cnt in cnts:
            if cv2.contourArea(cnt) < 10000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

    # Acumular los primeros 100 frames para promedios
    if frame_count < 100:
        for i in range(10):
            contour_history[i].append(contour_counts[i])
        if frame_count == 99:
            for i in range(10):
                avg_contours[i] = np.mean(contour_history[i])
            initialized = True
    else:
        if initialized:
            A1 = contour_counts[0] > avg_contours[0] * 1.5 if avg_contours[0] > 0 else False
            A2 = contour_counts[1] > avg_contours[1] * 1.5 if avg_contours[1] > 0 else False
            A3 = contour_counts[2] > avg_contours[2] * 1.5 if avg_contours[2] > 0 else False
            A4 = contour_counts[3] > avg_contours[3] * 1.5 if avg_contours[3] > 0 else False
            A5 = contour_counts[4] > avg_contours[4] * 1.5 if avg_contours[4] > 0 else False
            B1 = contour_counts[5] > avg_contours[5] * 1.5 if avg_contours[5] > 0 else False
            B2 = contour_counts[6] > avg_contours[6] * 1.5 if avg_contours[6] > 0 else False
            B3 = contour_counts[7] > avg_contours[7] * 1.5 if avg_contours[7] > 0 else False
            C1 = contour_counts[8] > avg_contours[8] * 1.5 if avg_contours[8] > 0 else False
            C2 = contour_counts[9] > avg_contours[9] * 1.5 if avg_contours[9] > 0 else False

    # Mostrar estado en pantalla
    cv2.putText(frame, f"A1:{A1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if A1 else (0,0,255), 2)
    cv2.putText(frame, f"A2:{A2}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if A2 else (0,0,255), 2)
    cv2.putText(frame, f"A3:{A3}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if A3 else (0,0,255), 2)
    cv2.putText(frame, f"A4:{A4}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if A4 else (0,0,255), 2)
    cv2.putText(frame, f"A5:{A5}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if A5 else (0,0,255), 2)
    cv2.putText(frame, f"B1:{B1}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if B1 else (0,0,255), 2)
    cv2.putText(frame, f"B2:{B2}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if B2 else (0,0,255), 2)
    cv2.putText(frame, f"B3:{B3}", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if B3 else (0,0,255), 2)
    cv2.putText(frame, f"C1:{C1}", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if C1 else (0,0,255), 2)
    cv2.putText(frame, f"C2:{C2}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0) if C2 else (0,0,255), 2)

    # Guardar el estado de los lugares en un archivo JSON cada 20 frames
    if frame_count % 20 == 0:
        spots_status = {
            "A1": bool(A1), "A2": bool(A2), "A3": bool(A3), "A4": bool(A4), "A5": bool(A5),
            "B1": bool(B1), "B2": bool(B2), "B3": bool(B3),
            "C1": bool(C1), "C2": bool(C2)
        }
        with open("spots_status.json", "w") as f:
            json.dump(spots_status, f)

    frame_count += 1  # <--- SIEMPRE INCREMENTA AQUÍ

    cv2.imshow("Video Output", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()