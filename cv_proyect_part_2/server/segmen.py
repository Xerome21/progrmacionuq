import cv2
import numpy as np
import os

# Folder to save segmented parts
output_folder = 'segments'

if not os.path.exists(output_folder):
    print('Folder created:', output_folder)
    os.makedirs(output_folder)

# Read the input image
img_input = cv2.imread(r"C:\Users\kkyto\Desktop\hrzone\opencv_proyect\cascade_training\parkinglot.jpg")

if img_input is None:
    print("Error: Image not found.")
    exit()

# Define the number of rows and columns for segmentation (inverted)
cols, rows = 2, 7  # Adjust these values as needed (swapped rows and cols)

# Get the dimensions of the image
height, width, _ = img_input.shape

# Calculate the height and width of each segment (inverted)
segment_height = height // rows
segment_width = width // cols

# Counter for naming the segmented parts
segment_counter = 0

# Loop through the grid and segment the image
for row in range(rows):
    for col in range(cols):
        # Calculate the coordinates of the current segment
        x1 = col * segment_width
        y1 = row * segment_height
        x2 = x1 + segment_width
        y2 = y1 + segment_height

        # Extract the segment
        segment = img_input[y1:y2, x1:x2]

        # Save the segment as an image
        segment_filename = f'{output_folder}/segment_{segment_counter}.jpg'
        cv2.imwrite(segment_filename, segment)
        print(f'Segment saved: {segment_filename}')
        segment_counter += 1

        # Display the segment (optional)
        cv2.imshow(f'Segment {segment_counter}', segment)

# Wait for the 'q' key to close all windows
print("Press 'q' to close all windows.")
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()