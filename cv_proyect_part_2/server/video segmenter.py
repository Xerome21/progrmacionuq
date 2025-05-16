import cv2
import numpy as np
import os

# Folder to save segmented parts
output_folder = 'video_segments'

if not os.path.exists(output_folder):
    print('Folder created:', output_folder)
    os.makedirs(output_folder)

# Read the input video
video_path = r"C:\Users\kkyto\Desktop\hrzone\opencv_proyect\cascade_training\parkinglot_video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Video not found or cannot be opened.")
    exit()

# Define the number of rows and columns for segmentation
rows, cols = 7, 2  # Adjust these values as needed

# Counter for naming the segmented parts
frame_counter = 0

# Resize scale (e.g., 0.5 for half the size)
resize_scale = 0.3

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read the frame.")
        break

    # Resize the frame to make it smaller
    frame = cv2.resize(frame, (0, 0), fx=resize_scale, fy=resize_scale)

    # Get the dimensions of the resized frame
    height, width, _ = frame.shape

    # Calculate the height and width of each segment
    segment_height = height // rows
    segment_width = width // cols

    # Loop through the grid and draw rectangles for each segment
    for row in range(rows):
        for col in range(cols):
            # Calculate the coordinates of the current segment
            x1 = col * segment_width
            y1 = row * segment_height
            x2 = x1 + segment_width
            y2 = y1 + segment_height

            # Draw a green rectangle around the segment
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the frame with rectangles
    cv2.imshow("Segmented Frame", frame)

    # Wait for the 'q' key to stop processing
    if cv2.waitKey(400) & 0xFF == ord('q'):
        break

    frame_counter += 1

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()