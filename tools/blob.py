import cv2
import numpy as np

# Step 1: Load the image
image = cv2.imread('media/lec-test.png')
image = cv2.resize(image, (224,224))

# Step 2: Convert to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Step 3: Define the color range and threshold the HSV image
# Example for detecting red color
lower_red = np.array([58, 63, 77])
upper_red = np.array([85, 91, 110])
mask1 = cv2.inRange(hsv_image, lower_red, upper_red)

lower_red = np.array([168, 120, 70])
upper_red = np.array([159, 154, 165])
mask2 = cv2.inRange(hsv_image, lower_red, upper_red)

mask = mask1 + mask2

# Step 4: Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Step 5: Draw contours
result_image = image.copy()
cv2.drawContours(result_image, contours, -1, (0, 255, 0), 3)

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Mask', mask)
cv2.imshow('Detected Blobs', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
