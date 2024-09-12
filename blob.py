import cv2
import numpy as np

# Step 1: Load the image
image = cv2.imread('media/input.png')
image = cv2.resize(image, (224,224))

cv2.rectangle(image, (0,0), (224,40), (0,0,0), -1)
cv2.rectangle(image, (0,180), (224,224), (0,0,0), -1)
image = cv2.GaussianBlur(image, (3, 3), 0)


# Step 2: Convert to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv', hsv_image)

# Step 3: Define the color range and threshold the HSV image
# Example for detecting red color

lower_white = (0,0,219)
upper_white = (37,14,255)

mask1 = cv2.inRange(hsv_image, lower_white, upper_white)
mask = mask1 

# Step 4: Find contours
#contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Step 5: Draw contours
#result_image = image.copy()
#cv2.drawContours(result_image, contours, -1, (0, 255, 0), 3)

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Mask', mask)
#cv2.imshow('Detected Blobs', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
