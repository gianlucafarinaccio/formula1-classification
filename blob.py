import cv2
import matplotlib.pyplot as plt
import numpy as np



# Definisci la funzione per la correzione gamma
def adjust_gamma(image, gamma=1.0):
    # Costruisci una lookup table per mappare ogni valore di pixel
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    # Applica la mappatura con la lookup table usando cv2.LUT
    return cv2.LUT(image, table)


IMAGE_DIM = (224,224)
cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])
aoi = np.array([[0,224],[224,224],[224,78],[160,48],[100,48],[0,132]])

# Step 1: Load the image and resize
image = cv2.imread('media/input.png')
image = cv2.resize(image, IMAGE_DIM)



# Applica la correzione gamma con un valore gamma (ad esempio, 2.2)
# gamma = adjust_gamma(np.copy(image), gamma=2.2)


# low_asfalto = (136, 0, 115)
# high_asfalto = (180, 45, 167)

# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# mask_asfalto = cv2.inRange(hsv_image, low_asfalto, high_asfalto)

# Step 2: Convert to Grayscale and apply gaussian blurring
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

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


# Step 4: Create a mask for my 'area of interest'
#aoi = np.ones(IMAGE_DIM, dtype=np.uint8)
# cv2.fillPoly(aoi, [cockpit], 0)
# cv2.fillPoly(aoi, [sky], 0)
# aoi = aoi * 255

# Step 5: Dilate the all white pixels found
erosion_kernel = np.ones((5,5), np.uint8)
dilated = cv2.dilate(mask, erosion_kernel, iterations = 1)
cv2.fillPoly(dilated, [cockpit], 0)
cv2.fillPoly(dilated, [sky], 0)


cv2.fillPoly(edges, [cockpit], 0)
cv2.fillPoly(edges, [sky], 0)
lines = np.zeros((224,224),dtype = np.uint8)
cv2.fillPoly(lines, [aoi], 255)
edges = cv2.bitwise_and(edges, lines)


dilated = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
enh = cv2.addWeighted(image, 1, dilated, 1, 0)


edges_and_mask = cv2.bitwise_and(edges, mask)

# Step 4: Hough Transform to detect and connect lines
rho = 1  # Distance resolution in pixels
theta = np.pi / 180  # Angular resolution in radians
threshold = 20  # Minimum number of votes in accumulator
min_line_length = 50  # Minimum length of a line (in pixels) to be accepted
max_line_gap = 10  # Maximum gap between segments to link them

liness = cv2.HoughLinesP(edges_and_mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

# Create an image to draw the lines
line_image = np.zeros((224,224), dtype = np.uint8)

# Draw lines
if liness is not None:
    for line in liness:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), 255, 3)


# Applica l'operazione bitwise_and
#masked_image = cv2.addWeighted(image,1, mask,1,0)
line_image = cv2.cvtColor(line_image, cv2.COLOR_GRAY2BGR)
mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
alls = cv2.addWeighted(image, 1, line_image, 1, 0)

masked_image = cv2.bitwise_and(alls,mask)



cv2.imshow('original', image)
cv2.imshow("edges_and_mask",edges_and_mask)
cv2.imshow('masked_image', masked_image)
cv2.imshow('line_image', line_image)

cv2.waitKey(0)
cv2.destroyAllWindows()











