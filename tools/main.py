import cv2
import time
import numpy as np

cap = cv2.VideoCapture('media/bottas.mp4')
print(cap.get(cv2.CAP_PROP_FPS))


frame_count = 0
prev_frame_time = 0
new_frame_time = 0

while cap.isOpened():
	ret, frame = cap.read()

	frame = cv2.resize(frame, (224,224))
	cv2.rectangle(frame, (0,0), (224,40), (0,0,0), -1)
	cv2.rectangle(frame, (0,180), (224,224), (0,0,0), -1)
	frame = cv2.GaussianBlur(frame, (3, 3), 0)
	result_image = frame.copy()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	lower_erba = (17,64,92)
	upper_erba = (42,152,211)

	lower_terra = (0,22,167)
	upper_terra = (31,55,216)	

	mask_erba = cv2.inRange(frame, lower_erba, upper_erba)
	mask_terra = cv2.inRange(frame, lower_terra, upper_terra)
	mask = mask_erba + mask_terra
	kernel = np.ones((5,5), np.uint8)  # Kernel 5x5

	#Applica l'erosione
	mask = cv2.erode(mask, kernel, iterations=1)


	#Step 4: Find contours
	contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#Step 5: Draw contours

	cv2.drawContours(result_image, contours, -1, (0, 0, 255), 5)

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break


	if frame_count % 2 == 0:
		cv2.imshow('Detected Blobs', result_image)
		cv2.imshow('Original Image', frame)
		#cv2.imshow('Mask', mask)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()

