import cv2 
import numpy as np
import imutils
import os

datos = 'n'

if not os.path.exists(datos):
    print('carpeta creada', datos)
    os.makedirs(datos)
    
video_input = cv2.VideoCapture('http://192.168.1.72:8080/video')

x1, y1 = 190, 80
x2, y2 = 280, 290

acco = 0

while True:
    ret, frame = video_input.read()
    
    if ret == False: break
    imAux = frame.copy()
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    obj = imAux[y1:y2, x1:x2]
    obj = imutils.resize(obj, width=38)
    
    k = cv2.waitKey(1)
    if k == 27: 
        break
    
    if k == ord('s'):
        cv2.imwrite(datos+'/objeto_{}.jpg'.format(acco), obj)
        print('Guardado exitoso: ', 'objeto_{}.jpg'.format(acco))
        acco += 1
        
    cv2.imshow('video', frame)
    cv2.imshow('objeto', obj)
    
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
    
video_input.release()
cv2.destroyAllWindows()