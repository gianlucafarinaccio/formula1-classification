import cv2
import matplotlib.pyplot as plt
import numpy as np


IMAGE_DIM = (224,224)
cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])

# Step 1: Load the image
image = cv2.imread('media/input.png')
image = cv2.resize(image, IMAGE_DIM)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

edges = cv2.Canny(gray_image,100,200)
mask = cv2.inRange(gray_image, 242, 255)

aoi = np.ones(IMAGE_DIM, dtype=np.uint8)
cv2.fillPoly(aoi, [cockpit], 0)
cv2.fillPoly(aoi, [sky], 0)
aoi = aoi * 255

erosion_kernel = np.ones((3,3), np.uint8)
erode = cv2.dilate(mask, erosion_kernel, iterations = 1)

res = cv2.bitwise_and(aoi, erode)

cv2.imshow('original', image)
cv2.imshow('processed', gray_image)
cv2.imshow('mask', mask)
cv2.imshow('aoi', aoi)
cv2.imshow('res', res)
cv2.imshow('erode', erode)
cv2.imshow('edges', edges)



# points = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])

# # Reshape the points for polylines function
# points = points.reshape((-1, 1, 2))

# cv2.rectangle(image, (0,0), (224,40), (0,0,0), -1)
# #cv2.rectangle(image, (0,180), (224,224), (0,0,0), -1)
# cv2.fillPoly(image, [points], color=(0, 0, 0))

# edges = cv2.Canny(image,100,200)

# # Step 2: Convert to HSV
# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# cv2.imshow('hsv', hsv_image)

# # Step 3: Define the color range and threshold the HSV image
# # Example for detecting red color

# lower_white = (0,0,219)
# upper_white = (37,14,255)

# mask = cv2.inRange(hsv_image, lower_white, upper_white)
# #mask = cv2.dilate(mask,mask) 

# # Step 4: Find contours
# contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# # Step 5: Draw contours
# result_image = image.copy()
# cv2.drawContours(result_image, contours, -1, (0, 0, 255), 5)

# # Display the results
# plt.imshow(image)
# plt.show()

# cv2.imshow('Original Image', image)
# cv2.imshow('Mask', mask)
# cv2.imshow('edges',edges)
# cv2.imshow('Detected Blobs', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()











