from ultralytics import YOLO
import cv2
import numpy as np


cap = cv2.VideoCapture('media/224_canny/bottas_224_canny.mp4')

frame_count = 0
model = YOLO("models/224_canny.pt")

cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])

while cap.isOpened():
	ret, image = cap.read()

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	if frame_count % 2 == 0:
		cv2.imwrite('run/img.png', image)
		pred = model('run/img.png')

		indice = pred[0].probs.top1
		classe = pred[0].names[indice]
		print(classe)

		image = cv2.putText(image, classe, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

		cv2.imshow('Original Image', image)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()
