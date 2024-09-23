import cv2
import argparse
import numpy as np

# Percorso del video di input
INPUT_VIDEO_FILE_PATH = "media/"

# Percorso del video di output
OUTPUT_VIDEO_FILE_PATH = "media/224_mask_no_filter"

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--i', type=str, required=True)
parser.add_argument('--o', type=str, required=True)
args = parser.parse_args()

INPUT_VIDEO_FILE_PATH = "media/" + args.i
OUTPUT_VIDEO_FILE_PATH = "media/" + args.o

print('* input file: ' + INPUT_VIDEO_FILE_PATH)
print('** output file: ' + OUTPUT_VIDEO_FILE_PATH)


OUTPUT_RESOLUTION = (224, 224)

# Crea un oggetto VideoCapture per leggere il video
cap = cv2.VideoCapture(INPUT_VIDEO_FILE_PATH)

# Verifica se il video è stato aperto correttamente
if not cap.isOpened():
    print("Errore nell'apertura del file video")
    exit()


original_fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f'original fps: {original_fps}')
if(original_fps < 49):
    frame_scaler = 1
else:
    frame_scaler = 2

# Crea un oggetto VideoWriter per salvare il video con i nuovi FPS
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(OUTPUT_VIDEO_FILE_PATH, fourcc, 25.0, OUTPUT_RESOLUTION, isColor = True)

frame_count = 0


cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])
aoi = np.array([[0,224],[224,224],[224,78],[160,48],[100,48],[0,132]])

while True:
    # Leggi un frame dal video
    ret, frame = cap.read()

    # Se il frame non è stato letto correttamente, esci dal ciclo
    if not ret:
        break

    # Seleziona i frame necessari in base all'intervallo calcolato
    if (frame_count % frame_scaler) == 0:
        frame = cv2.resize(frame, OUTPUT_RESOLUTION)
        #frame = cv2.bilateralFilter(frame,9,75,75)

       # Step 2: Convert to Grayscale and apply gaussian blurring
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

        # Step 3: Highlight edges and select only white pixels
        edges = cv2.Canny(gray_image,100,200)
        mask = cv2.inRange(gray_image, 242, 255)

        # Step 4: Create a mask for my 'area of interest'
        #aoi = np.ones(IMAGE_DIM, dtype=np.uint8)
        # cv2.fillPoly(aoi, [cockpit], 0)
        # cv2.fillPoly(aoi, [sky], 0)
        # aoi = aoi * 255

        # Step 5: Dilate the all white pixels found
        erosion_kernel = np.ones((5,5), np.uint8)
        dilated = cv2.dilate(mask, erosion_kernel, iterations = 1)
        cv2.fillPoly(dilated, [cockpit], 0)
        cv2.fillPoly(dilated, [sky], 0)


        cv2.fillPoly(edges, [cockpit], 0)
        cv2.fillPoly(edges, [sky], 0)
        lines = np.zeros((224,224),dtype = np.uint8)
        cv2.fillPoly(lines, [aoi], 255)
        edges = cv2.bitwise_and(edges, lines)


        dilated = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
        enh = cv2.addWeighted(frame, 1, dilated, 1, 0)


        edges_and_mask = cv2.bitwise_and(edges, mask)

        # Step 4: Hough Transform to detect and connect lines
        rho = 1  # Distance resolution in pixels
        theta = np.pi / 180  # Angular resolution in radians
        threshold = 20  # Minimum number of votes in accumulator
        min_line_length = 50  # Minimum length of a line (in pixels) to be accepted
        max_line_gap = 10  # Maximum gap between segments to link them

        liness = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

        # Create an image to draw the lines
        line_image = np.zeros((224,224), dtype = np.uint8)

        # Draw lines
        if liness is not None:
            for line in liness:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), 255, 3)


        #res = cv2.bitwise_and(res, line_image)
        line_image = cv2.cvtColor(line_image, cv2.COLOR_GRAY2BGR)
        alls = cv2.addWeighted(frame, 1, line_image, 1, 0)

        out.write(alls)

    frame_count += 1

# Rilascia gli oggetti VideoCapture e VideoWriter
cap.release()
out.release()

print("*** Video processed ...")


