import cv2
import argparse

# Percorso del video di input
INPUT_VIDEO_FILE_PATH = "media/"

# Percorso del video di output
OUTPUT_VIDEO_FILE_PATH = "media/"

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--i', type=str, required=True)
parser.add_argument('--o', type=str, required=True)
args = parser.parse_args()

INPUT_VIDEO_FILE_PATH = "media/" + args.i
OUTPUT_VIDEO_FILE_PATH = "media/" + args.o

print('* input file: ' + INPUT_VIDEO_FILE_PATH)
print('** output file: ' + OUTPUT_VIDEO_FILE_PATH)


OUTPUT_RESOLUTION = (640, 640)

# Crea un oggetto VideoCapture per leggere il video
cap = cv2.VideoCapture(INPUT_VIDEO_FILE_PATH)

# Verifica se il video è stato aperto correttamente
if not cap.isOpened():
    print("Errore nell'apertura del file video")
    exit()


original_fps = int(cap.get(cv2.CAP_PROP_FPS))
if(original_fps < 49):
    frame_scaler = 1
else:
    frame_scaler = 2

# Crea un oggetto VideoWriter per salvare il video con i nuovi FPS
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(OUTPUT_VIDEO_FILE_PATH, fourcc, new_fps, OUTPUT_RESOLUTION, isColor = True)

frame_count = 0

while True:
    # Leggi un frame dal video
    ret, frame = cap.read()

    # Se il frame non è stato letto correttamente, esci dal ciclo
    if not ret:
        break

    # Seleziona i frame necessari in base all'intervallo calcolato
    if (frame_count % frame_scaler) == 0:
        frame = cv2.resize(frame, OUTPUT_RESOLUTION)
        frame = cv2.bilateralFilter(frame,9,75,75)

        out.write(frame)

    frame_count += 1

# Rilascia gli oggetti VideoCapture e VideoWriter
cap.release()
out.release()

print("*** Video processed ...")


