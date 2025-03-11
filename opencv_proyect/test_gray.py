
import cv2

img = cv2.imread("gray.bmp",cv2.IMREAD_GRAYSCALE)

dims=img.shape


print(f'Image has s{dims[0]} rows and {dims[1]} columns')

cv2.imshow("image", img)


print(img)

cv2.waitKey()
     
    

