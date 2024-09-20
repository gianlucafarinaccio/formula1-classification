from ultralytics import YOLO
import cv2
import numpy as np


cap = cv2.VideoCapture('media/224_mask_no_filter/bottas_224_mask_no_filter.mp4')

frame_count = 0
model = YOLO("models/224_mask_no_filter_v2.pt")

cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])

while cap.isOpened():
	ret, frame = cap.read()

	# frame = cv2.resize(frame, (224,224))
	# cv2.fillPoly(frame, [cockpit], 0)
	# cv2.fillPoly(frame, [sky], 0)

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	if frame_count % 2 == 0:
		cv2.imwrite('run/img.png', frame)
		pred = model('run/img.png')

		indice = pred[0].probs.top1
		classe = pred[0].names[indice]
		print(classe)

		cv2.imshow('Original Image', frame)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()
