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

edges = cv2.Canny(image,100,200)

# Step 3: Define the color range and threshold the HSV image
# Example for detecting red color
"""
Determine and cut the region of interest in the input image.
Parameters:
	image: we pass here the output from canny where we have 
	identified edges in the frame
"""
# create an array of the same size as of the input image 
mask = np.zeros_like(edges) 
# if you pass an image with more then one channel
if len(edges.shape) > 2:
	channel_count = edges.shape[2]
	ignore_mask_color = (255,) * channel_count
# our image only has one channel so it will go under "else"
else:
	# color of the mask polygon (white)
	ignore_mask_color = 255
# creating a polygon to focus only on the road in the picture
# we have created this polygon in accordance to how the camera was placed

vertices = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
# filling the polygon with white color and generating the final mask
cv2.fillPoly(mask, [vertices], ignore_mask_color)
mask = cv2.bitwise_not(mask)
# performing Bitwise AND on the input image and mask to get only the edges on the road
masked_edges = cv2.bitwise_and(edges, mask)


mask2 = np.zeros_like(edges) 
vertices2 = np.array([[5, 82], [0, 222], [222, 215], [222, 83]])
cv2.fillPoly(mask2, [vertices2], ignore_mask_color)
masked_edges2 = cv2.bitwise_and(masked_edges, mask2)


# Step 4: Hough Transform to detect and connect lines
rho = 1  # Distance resolution in pixels
theta = np.pi / 180  # Angular resolution in radians
threshold = 20  # Minimum number of votes in accumulator
min_line_length = 40  # Minimum length of a line (in pixels) to be accepted
max_line_gap = 300  # Maximum gap between segments to link them

lines = cv2.HoughLinesP(masked_edges2, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

# Create an image to draw the lines
line_image = np.copy(masked_edges2) * 0  # Create a black image

# Draw lines
if lines is not None:
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), [255, 0, 0], 5)

# Combine original image with the line image
masked_image = cv2.addWeighted(masked_edges2, 0.8, line_image, 1, 0)

if len(masked_image.shape) == 2:  # Check if it's single channel
    masked_image_color = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)  # Convert to 3 channels
else:
    masked_image_color = masked_image # It's already 3 channels


combined_image = cv2.addWeighted(image, 0.8, masked_image_color, 1, 0)

white_mask = np.all(combined_image == [255, 255, 255], axis=-1)
output_image = combined_image.copy()
output_image[white_mask] = [0, 0, 255]


# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Mask', mask)
cv2.imshow("edges",edges)
cv2.imshow("masked_edges",masked_edges)
cv2.imshow("masked_edges2",masked_edges2)
cv2.imshow('masked Image', masked_image)
cv2.imshow('combined_image', combined_image)
cv2.imshow('output_image',output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()