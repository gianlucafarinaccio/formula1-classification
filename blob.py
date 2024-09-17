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

# Step 1: Load the image and resize
image = cv2.imread('media/input.png')
image = cv2.resize(image, IMAGE_DIM)


# Applica la correzione gamma con un valore gamma (ad esempio, 2.2)
gamma = adjust_gamma(np.copy(image), gamma=2.2)


low_asfalto = (136, 0, 115)
high_asfalto = (180, 45, 167)

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask_asfalto = cv2.inRange(hsv_image, low_asfalto, high_asfalto)

# Step 2: Convert to Grayscale and apply gaussian blurring
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

# Step 3: Highlight edges and select only white pixels
edges = cv2.Canny(gray_image,100,200)
mask = cv2.inRange(gray_image, 242, 255)

# Step 4: Create a mask for my 'area of interest'
aoi = np.ones(IMAGE_DIM, dtype=np.uint8)
cv2.fillPoly(aoi, [cockpit], 0)
cv2.fillPoly(aoi, [sky], 0)
aoi = aoi * 255

# Step 5: Dilate the all white pixels found
erosion_kernel = np.ones((3,3), np.uint8)
dilated = cv2.dilate(mask, erosion_kernel, iterations = 1)


eroded_asfalto = cv2.erode(mask_asfalto, erosion_kernel, iterations = 1)
eroded_asfalto = cv2.bitwise_and(aoi, eroded_asfalto)
eroded_asfalto = cv2.dilate(eroded_asfalto, erosion_kernel, iterations = 3)

res = cv2.bitwise_and(aoi, dilated)
edges = cv2.bitwise_and(aoi,edges)

blob_asfalto = np.zeros((224,224,3), dtype = np.uint8)
blob_asfalto[:,:,0] = eroded_asfalto


# Step 4: Hough Transform to detect and connect lines
rho = 1  # Distance resolution in pixels
theta = np.pi / 180  # Angular resolution in radians
threshold = 20  # Minimum number of votes in accumulator
min_line_length = 50  # Minimum length of a line (in pixels) to be accepted
max_line_gap = 10  # Maximum gap between segments to link them

lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

# Create an image to draw the lines
line_image = np.zeros((224,224), dtype = np.uint8)

# Draw lines
if lines is not None:
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), 255, 3)


res = cv2.bitwise_and(res, line_image)
alls = cv2.addWeighted(blob_asfalto, 1, image, 1, 0)


cv2.imshow('original', image)
cv2.imshow('gamma', gamma)
#cv2.imshow('processed', gray_image)
cv2.imshow('mask_asfalto', blob_asfalto)
cv2.imshow('alls', alls)
#cv2.imshow('mask', mask)
#cv2.imshow('aoi', aoi)
cv2.imshow('res', res)
#cv2.imshow('dilated', dilated)
cv2.imshow('edges', edges)
cv2.imshow('line_image', line_image)



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











