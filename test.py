import cv2

# Percorso del video di input
input_video_path = 'media/hamilton.mp4'

# Percorso del video di output
output_video_path = 'media/hamilton-reduced.mp4'

# Nuovi FPS desiderati
new_fps = 25

# Crea un oggetto VideoCapture per leggere il video
cap = cv2.VideoCapture(input_video_path)

# Verifica se il video è stato aperto correttamente
if not cap.isOpened():
    print("Errore nell'apertura del file video")
    exit()

# Ottieni i parametri del video originale
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
original_fps = cap.get(cv2.CAP_PROP_FPS)

# Calcola l'intervallo di frame da mantenere per ottenere i nuovi FPS
frame_interval = int(original_fps / new_fps)

# Crea un oggetto VideoWriter per salvare il video con i nuovi FPS
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, new_fps, (320, 240))

frame_count = 0

while True:
    # Leggi un frame dal video
    ret, frame = cap.read()

    # Se il frame non è stato letto correttamente, esci dal ciclo
    if not ret:
        break

    # Seleziona i frame necessari in base all'intervallo calcolato
    if (frame_count % 2) == 0:
        frame = cv2.resize(frame, (320,240))
        out.write(frame)

    frame_count += 1

# Rilascia gli oggetti VideoCapture e VideoWriter
cap.release()
out.release()

print("Il video è stato salvato con i nuovi FPS correttamente.")
