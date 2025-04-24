import cv2

video = cv2.VideoCapture('http://192.168.1.72:8080/video')

# Load the cascade classifier with an absolute path
cascade_path = r'C:\Users\kkyto\Desktop\hrzone\opencv_proyect\cascade_training\cascade.xml'
CarClasiff = cv2.CascadeClassifier(cascade_path)

# Check if the cascade file loaded correctly
if CarClasiff.empty():
    print(f"Error: Unable to load cascade file: {cascade_path}")
    exit()

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Couldn't read the video stream")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    carro = CarClasiff.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10)
    
    for (x, y, w, h) in carro:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Carro', (x, y-10), 2, 0.7, (0,255,0), 2, cv2.LINE_AA)
        
    cv2.imshow('Output', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
