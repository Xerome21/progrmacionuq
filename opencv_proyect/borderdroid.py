# iciamos la cámara
import numpy as np
import cv2

video = cv2.VideoCapture('http://192.168.1.72:8080/video')

while (video.isOpened()):
    ret, frame = video.read()
    
    if (ret==True):
        #aplicar canny
        grises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grises, (5, 5), 0)
        bordeCanny = cv2.Canny(blur, 100, 200)
        
        ctns, _ = cv2.findContours(bordeCanny, cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(frame, ctns, -1, (0, 0, 255), 2)
        
        cv2.imshow(' video de entrada', frame)
        cv2.imshow(' grises', grises)
        cv2.imshow(' blur', blur)
        cv2.imshow(' bordes', bordeCanny)
        
        print('numero de contornos encontrados', len(ctns))
        
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
    else:
        break
# fin de inicio de camara





video.release()
cv2.destroyAllWindows()