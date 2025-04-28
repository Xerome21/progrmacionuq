# iciamos la cámara
import numpy as np
import cv2

video = cv2.VideoCapture(r'C:\Users\kkyto\Desktop\hrzone\opencv_proyect\cv_proyect_part_2\parkinglot_video.mp4')

while (video.isOpened()):
    ret, frame = video.read()
    
    if (ret==True):
        #aplicar canny
        grises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grises, (5, 5), 0)
        bordeCanny = cv2.Canny(blur, 75, 100)
        
        ctns, _ = cv2.findContours(bordeCanny, cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(frame, ctns, -1, (0, 0, 255), 2)
        
        rezise_1 = cv2.resize(frame, (360, 640))
        rezise_2 = cv2.resize(grises, (360, 640))
        rezise_3 = cv2.resize(blur, (360, 640)) 
        rezise_4 = cv2.resize(bordeCanny, (360, 640))
        
        cv2.imshow(' video de entrada', rezise_1)
        cv2.imshow(' grises', rezise_2)
        cv2.imshow(' blur', rezise_3)
        cv2.imshow(' bordes', rezise_4)
        
        print('numero de contornos encontrados', len(ctns))
        
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
    else:
        break
# fin de inicio de camara





video.release()
cv2.destroyAllWindows()