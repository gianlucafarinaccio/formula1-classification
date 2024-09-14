import cv2
import time
import numpy as np

cap = cv2.VideoCapture('media/bottas.mp4')
print(cap.get(cv2.CAP_PROP_FPS))

frame_count = 0
prev_frame_time = 0
new_frame_time = 0

IMAGE_DIM = (224,224)
cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])

aoi = np.ones(IMAGE_DIM, dtype=np.uint8)
cv2.fillPoly(aoi, [cockpit], 0)
cv2.fillPoly(aoi, [sky], 0)
aoi = aoi * 255

while cap.isOpened():
	ret, image = cap.read()
	image = cv2.resize(image, IMAGE_DIM)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

	edges = cv2.Canny(gray_image,100,200)
	mask = cv2.inRange(gray_image, 242, 255)

	erosion_kernel = np.ones((3,3), np.uint8)
	erode = cv2.dilate(mask, erosion_kernel, iterations = 1)

	res = cv2.bitwise_and(aoi, erode)
	
	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break


	if frame_count % 2 == 0:
		cv2.imshow('res', res)
		cv2.imshow('Original Image', image)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()