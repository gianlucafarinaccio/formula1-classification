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
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_white = (15,60,96)
	upper_white = (38,124,201)

	mask = cv2.inRange(frame, lower_white, upper_white)

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break


	if frame_count % 2 == 0:
		cv2.imshow('Original Image', frame)
		cv2.imshow('Mask', mask)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()

