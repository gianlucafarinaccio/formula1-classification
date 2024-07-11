import cv2
import time
import numpy as np

cap = cv2.VideoCapture('media/leclerc.mp4')
print(cap.get(cv2.CAP_PROP_FPS))


frame_count = 0
prev_frame_time = 0
new_frame_time = 0

while cap.isOpened():
	ret, frame = cap.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	frame[..., 2] = cv2.subtract(frame[..., 2], 50)
	frame = cv2.resize(frame, (224,224))

	cv2.rectangle(frame, (50,100), (180,120), (0,0,0), -1)
	cv2.rectangle(frame, (0,120), (224,224), (0,0,0), -1)
	frame = cv2.GaussianBlur(frame, (3, 3), 0)

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break


	if frame_count % 2 == 0:
		cv2.imshow('frame', frame)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()

