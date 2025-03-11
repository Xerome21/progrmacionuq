# Import OpenCV module
import cv2
import numpy as np

# Function to calculate the mean of a plane
def calculate_mean(plane):
    return plane.mean()

def create_planes(img):
    bluePlane = img[:, :, 0]
    greenPlane = img[:, :, 1]
    redPlane = img[:, :, 2]

    return bluePlane, greenPlane, redPlane


# Function to identify the color of the car
def identifyColor(img):
    bluePlane, greenPlane, redPlane = create_planes(img)
    
    # Calculate the mean of each color plane
    blue_mean = calculate_mean(bluePlane)
    green_mean = calculate_mean(greenPlane)
    red_mean = calculate_mean(redPlane)

    # Determine the dominant color
    if blue_mean > green_mean and blue_mean > red_mean:
        return "Blue"
    elif green_mean > blue_mean and green_mean > red_mean:
        return "Green"
    else:
        return "Red"

# Ask the user for the image name
image_name = input("Enter the image name (blue_car.jfif, red_car.jfif, or yellow_car.jfif): ")

# Read the image
img = cv2.imread(image_name, cv2.IMREAD_COLOR)

# Check if the image was successfully loaded
if img is None:
    print("Error: Could not load image.")
else:
    # Identify the color of the car
    color = identifyColor(img)
    print(f'The color of the car is: {color}')
    
    # Get matrix for each color plane
    bluePlane, greenPlane, redPlane = create_planes(img)
    
    # Stack the images horizontally
    combined_image = np.hstack((img, cv2.merge([bluePlane, bluePlane, bluePlane]), cv2.merge([greenPlane, greenPlane, greenPlane]), cv2.merge([redPlane, redPlane, redPlane])))

    # Display the combined image
    frame = cv2.resize(combined_image, (664, 290))
    cv2.namedWindow("Combined Image")
    cv2.imshow("Combined Image", frame)
    cv2.moveWindow("Combined Image", 400, 200)
    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()