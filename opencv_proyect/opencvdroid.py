# miciamos la cámara


import cv2
video = cv2.VideoCapture('http://192.168.1.72:8080/video')

while (video.isOpened()):
    ret, frame = video.read()
    
    if (ret==True):
        cv2.imshow(' video de entrada',frame)
        
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
    else:
        break

video.release()
cv2.destroyAllWindows()