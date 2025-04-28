import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(r"C:\Users\kkyto\Desktop\hrzone\opencv_proyect\cv_proyect_part_2\parkinglot_video.mp4")  # Ruta corregida para tu archivo subido

bgsub = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))   
fgbg = cv2.createBackgroundSubtractorMOG2()

car_setter = False

while True: 
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = imutils.resize(frame, width=360)
    
    area = np.array([[100, 360], [frame.shape[1]-100, 360], [frame.shape[1]-100, 430], [100, 430]])
    
    imAux = np.zeros(shape=(frame.shape[:2]), dtype = np.uint8)
    imAux = cv2.drawContours(imAux, [area], -1, (255), -1)
    sensible_area = cv2.bitwise_and(frame, frame, mask=imAux)
    
    cv2.drawContours(frame, [area], -1, (255,0,255))
    cv2.line(frame, (175, 360), (175, 430), (0, 255, 255), 2) 
    bgmask = fgbg.apply(sensible_area)
    bgmask = cv2.morphologyEx(bgmask, cv2.MORPH_OPEN, kernel)
    bgmask = cv2.morphologyEx(bgmask, cv2.MORPH_CLOSE, kernel)
    bgmask = cv2.dilate(bgmask, None, iterations=5)
    
    cnts = cv2.findContours(bgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    car_detected = False  # Temporary variable to track if a car is detected in this frame
    for cnt in cnts:
        if cv2.contourArea(cnt) < 15000:
            continue
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        car_detected = True  # A car is detected in this frame
        cv2.putText(frame, "Car detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Update the car_setter variable based on whether a car was detected
    car_setter = car_detected

    # Display the car_setter status on the frame
    status_text = "Car Present" if car_setter else "No Car"
    cv2.putText(frame, f"Status: {status_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    x1, y1 = 100, 360
    x2, y2 = 250, 430

    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Dibujamos en verde
    
    cv2.imshow("Video output", frame)
    cv2.imshow("Area sensible", imAux)
    cv2.imshow("toggle", sensible_area)
    cv2.imshow("Background Subtractor", bgmask)
    
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
