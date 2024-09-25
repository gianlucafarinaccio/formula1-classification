from ultralytics import YOLO
import cv2
import numpy as np


cap = cv2.VideoCapture('media/224_hist/bottas_224_hist.mp4')

frame_count = 0
model = YOLO("models/224_hist.pt")

cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])

while cap.isOpened():
	ret, image = cap.read()

	image = cv2.resize(image, (224,224))
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# Estrai il canale H (Hue)
	h_channel = hsv_image[:, :, 2]

	# Scala il canale H da [0, 179] a [0, 255]
	h_scaled = cv2.normalize(h_channel, None, 0, 255, cv2.NORM_MINMAX)

	# Applica l'equalizzazione dell'istogramma
	h_equalized = cv2.equalizeHist(h_scaled)

	# Scala nuovamente il canale H equalizzato da [0, 255] a [0, 179]
	h_equalized_scaled = cv2.normalize(h_equalized, None, 0, 179, cv2.NORM_MINMAX)

	# Sostituisci il canale H equalizzato nell'immagine HSV
	hsv_image[:, :, 2] = h_equalized_scaled

	# Converti l'immagine HSV modificata nuovamente a BGR
	equalized_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

	cv2.fillPoly(equalized_image, [cockpit], 0)
	cv2.fillPoly(equalized_image, [sky], 0)

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	if frame_count % 2 == 0:
		cv2.imwrite('run/img.png', equalized_image)
		pred = model('run/img.png')

		indice = pred[0].probs.top1
		classe = pred[0].names[indice]
		print(classe)

		cv2.imshow('Original Image', equalized_image)


	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()
