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


# Step 2: Convert to Grayscale and apply gaussian blurring
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

# Step 3: Highlight edges and select only white pixels
mask = cv2.inRange(gray_image, 242, 255)


# Step 5: Dilate the all white pixels found
erosion_kernel = np.ones((5,5), np.uint8)
dilated = cv2.dilate(mask, erosion_kernel, iterations = 1)
cv2.fillPoly(dilated, [cockpit], 0)
cv2.fillPoly(dilated, [sky], 0)

edges = cv2.Canny(gray_image,100,200)
cv2.fillPoly(edges, [cockpit], 0)
cv2.fillPoly(edges, [sky], 0)

lines = np.zeros((224,224),dtype = np.uint8)
cv2.fillPoly(lines, [aoi], 255)
dilated = cv2.bitwise_and(dilated, lines)

edges = cv2.bitwise_and(edges, lines)


# Step 4: Hough Transform to detect and connect lines
rho = 1  # Distance resolution in pixels
theta = np.pi / 180  # Angular resolution in radians
threshold = 20  # Minimum number of votes in accumulator
min_line_length = 50  # Minimum length of a line (in pixels) to be accepted
max_line_gap = 10  # Maximum gap between segments to link them

liness = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

# Create an image to draw the lines
line_image = np.zeros((224,224), dtype = np.uint8)

# Draw lines
if liness is not None:
    for line in liness:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), 255, 3)


res = cv2.bitwise_and(line_image, dilated)
res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
alls = cv2.addWeighted(image, 1, res, 1, 0)


cv2.imshow('image', image)
cv2.imshow('dilated', dilated)
cv2.imshow('edges', edges)
cv2.imshow('alls',alls)

cv2.waitKey(0)
cv2.destroyAllWindows()











