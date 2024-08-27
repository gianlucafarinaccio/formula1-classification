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


# Nuovi FPS desiderati
new_fps = 25

OUTPUT_RESOLUTION = (224, 224)

# Crea un oggetto VideoCapture per leggere il video
cap = cv2.VideoCapture(INPUT_VIDEO_FILE_PATH)

# Verifica se il video è stato aperto correttamente
if not cap.isOpened():
    print("Errore nell'apertura del file video")
    exit()

# Ottieni i parametri del video originale
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
original_fps = int(cap.get(cv2.CAP_PROP_FPS))

print(original_fps)
print(new_fps)
print(int(original_fps/new_fps))

# Calcola l'intervallo di frame da mantenere per ottenere i nuovi FPS
frame_interval = int(original_fps / new_fps)

print(frame_interval, original_fps)

# Crea un oggetto VideoWriter per salvare il video con i nuovi FPS
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(OUTPUT_VIDEO_FILE_PATH, fourcc, new_fps, OUTPUT_RESOLUTION, isColor = False)

frame_count = 0

while True:
    # Leggi un frame dal video
    ret, frame = cap.read()

    # Se il frame non è stato letto correttamente, esci dal ciclo
    if not ret:
        break

    # Seleziona i frame necessari in base all'intervallo calcolato
    if (frame_count % 2) == 0:
        frame = cv2.resize(frame, OUTPUT_RESOLUTION)
        cv2.rectangle(frame, (50,100), (180,120), (0,0,0), -1)
        cv2.rectangle(frame, (0,120), (224,224), (0,0,0), -1)
        frame = cv2.GaussianBlur(frame, (3, 3), 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame[..., 2] = cv2.subtract(frame[..., 2], 50)
        out.write(frame)

    frame_count += 1

# Rilascia gli oggetti VideoCapture e VideoWriter
cap.release()
out.release()

print("*** Video processed ...")
