import cv2
import json
import argparse

INPUT_VIDEO_FILE_PATH = "media/224_hist/"
OUTPUT_FILE_PATH = "f1-monza-dataset_224_hist/images/"
DRIVER_NAME = ""
TIMINGS_FILE_PATH = "timings/"
turns = ["neutro-zero","prima-variante", "neutro-uno","biassono","neutro-due" ,"seconda-variante","neutro-tre","lesmo-uno", "lesmo-due", "neutro-quattro","ascari-uno", "ascari-due", "neutro-cinque","parabolica", "neutro-sei"]

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--i', type=str, required=True)
parser.add_argument('--driver', type=str, required=True)
parser.add_argument('--timings', type=str, required=True)
args = parser.parse_args()

INPUT_VIDEO_FILE_PATH = INPUT_VIDEO_FILE_PATH + args.i
DRIVER_NAME = args.driver
TIMINGS_FILE_PATH = TIMINGS_FILE_PATH + args.timings

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
totals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
while cap.isOpened():
	ret, frame = cap.read()

	# if frame is read correctly ret is True
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	if (frame_count >= intervals[k][0]) and (frame_count <= intervals[k][1]):
		frame_id = DRIVER_NAME +'__' +str(k) +'__' + str(frame_count)
		path = OUTPUT_FILE_PATH+frame_id+'.jpg'
		totals[k] = totals[k] + 1 
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

with open("f1-monza-dataset_224_hist/stats.txt", 'a') as file:
	file.write(f'=============================\n\n')
	file.write(f'driver name: {DRIVER_NAME}\n')
	file.write(f'total frame: {frame_count}\n')
	for i,e in enumerate(totals):
		file.write(f'turn: {i} --> {e}\n')

