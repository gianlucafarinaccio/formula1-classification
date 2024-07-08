import cv2
import time

cap = cv2.VideoCapture('media/hamilton-reduced.mp4')
print(cap.get(cv2.CAP_PROP_FPS))


frame_count = 0
prev_frame_time = 0
new_frame_time = 0

while cap.isOpened():
	ret, frame = cap.read()
	frame = cv2.resize(frame, (320,240))
	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break


	if frame_count % 2 == 0:
		cv2.imshow('frame', frame)

	new_frame_time = time.time()

	# Calcola gli FPS
	fps = 1 / (new_frame_time - prev_frame_time)
	prev_frame_time = new_frame_time

	# Converti gli FPS a un intero
	fps = int(fps)

	# Converte gli FPS a stringa
	fps_str = f'FPS: {fps}'

	print(fps_str)

	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()