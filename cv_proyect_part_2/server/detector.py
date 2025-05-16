import cv2
import numpy as np
import imutils

# Load the video
cap = cv2.VideoCapture(r"C:\Users\kkyto\Desktop\hrzone\opencv_proyect\cv_proyect_part_2\parkinglot_video.mp4")

# Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Kernel for morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# Variable to track car presence
car_setter = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame for consistent processing
    frame = imutils.resize(frame, width=360)

    # Define the parking area (region of interest)
    area = np.array([[100, 360], [frame.shape[1] - 100, 360], [frame.shape[1] - 100, 430], [100, 430]])

    # Create a mask for the parking area
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area], -1, (255), -1)
    sensible_area = cv2.bitwise_and(frame, frame, mask=imAux)

    # Apply background subtraction
    bgmask = fgbg.apply(sensible_area)
    bgmask = cv2.morphologyEx(bgmask, cv2.MORPH_OPEN, kernel)
    bgmask = cv2.morphologyEx(bgmask, cv2.MORPH_CLOSE, kernel)
    bgmask = cv2.dilate(bgmask, None, iterations=5)

    # Find contours in the background-subtracted image
    cnts, _ = cv2.findContours(bgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize car detection flag
    car_detected = False

    for cnt in cnts:
                if cv2.contourArea(cnt) < 15000:
                    x,y,w,h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        
    # Update the car_setter variable based on detection
    

    # Display the car_setter status on the frame
    status_text = "Car Present" if car_setter else "No Car"
    cv2.putText(frame, f"Status: {status_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Draw the parking area on the frame
    cv2.drawContours(frame, [area], -1, (255, 0, 255), 2)

    # Display the frames
    cv2.imshow("Video Output", frame)
    cv2.imshow("Background Subtraction", bgmask)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()