import cv2
import time
import numpy as np



# Definisci la funzione per la correzione gamma
def adjust_gamma(image, gamma=1.0):
    # Costruisci una lookup table per mappare ogni valore di pixel
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    # Applica la mappatura con la lookup table usando cv2.LUT
    return cv2.LUT(image, table)


cap = cv2.VideoCapture('media/224_mask_no_filter/bottas_224_mask_no_filter.mp4')
print(cap.get(cv2.CAP_PROP_FPS))

frame_count = 0
prev_frame_time = 0
new_frame_time = 0

IMAGE_DIM = (224,224)
cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])
aoi = np.array([[0,224],[224,224],[224,78],[160,60],[100,60],[0,132]])

while cap.isOpened():
	ret, image = cap.read()
	image = cv2.resize(image, IMAGE_DIM)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	edges = cv2.Canny(image,100,200)
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

	
	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break


	if frame_count % 2 == 0:
		cv2.imshow('res', res)
		cv2.imshow('edges', edges)
		cv2.imshow('original', image)
		cv2.imshow('lines', alls)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()