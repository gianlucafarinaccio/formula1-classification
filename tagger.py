import cv2
import json
import argparse

INPUT_VIDEO_FILE_PATH = "media/"
OUTPUT_FILE_PATH = "data/"
DRIVER_NAME = ""
TIMINGS_FILE_PATH = ""
turns = ["prima-variante", "biassono", "seconda-variante","lesmo-uno", "lesmo-due", "ascari-uno", "ascari-due", "parabolica"]

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--i', type=str, required=True)
parser.add_argument('--o', type=str, required=True)
parser.add_argument('--driver', type=str, required=True)
parser.add_argument('--timings', type=str, required=True)
args = parser.parse_args()

INPUT_VIDEO_FILE_PATH = INPUT_VIDEO_FILE_PATH + args.i
OUTPUT_VIDEO_FILE_PATH = OUTPUT_VIDEO_FILE_PATH + args.o
DRIVER_NAME = args.driver
TIMINGS_FILE_PATH = args.timings

# 1. read json file 
timings = {}
with open(TIMINGS_FILE_PATH) as file:
	timings = json.load(file)


intervals = []
cap = cv2.VideoCapture(INPUT_VIDEO_FILE_PATH) #open video
fps = cap.get(cv2.CAP_PROP_FPS) #read fps

# create list of tuple [(1,2),(4,5)..]
for value in timings.values():
	tup = (int(value['interval'][0] *fps), int(value['interval'][1] *fps))
	intervals.insert(value['id'], tup)

frame_count = 0
k = 0
while cap.isOpened():
	ret, frame = cap.read()

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	if (frame_count >= intervals[k][0]) and (frame_count <= intervals[k][1]):
		frame_id = DRIVER_NAME +'__' +str(k) +'__' + str(frame_count)
		path = OUTPUT_FILE_PATH+turns[k]+'/'+DRIVER_NAME+'/'+frame_id+'.jpg'
		cv2.imwrite(path,frame)
	
	elif frame_count >= intervals[len(intervals)-1][1]:
		break
		
	elif frame_count >= intervals[k][1]:
		k+=1

	if cv2.waitKey(1) == ord('q'):
		break

	frame_count += 1
cap.release()
cv2.destroyAllWindows()


