import cv2
import numpy as np


def nothing(x):
    pass

def main():


    img = np.zeros((300, 512, 3), np.uint8)
    cv2.namedWindow('image')

    cv2.createTrackbar('H_HIGH', 'image', 0, 180, nothing)
    cv2.createTrackbar('S_HIGH', 'image', 0, 255, nothing)
    cv2.createTrackbar('V_HIGH', 'image', 0, 255, nothing)
    cv2.createTrackbar('H_LOW', 'image', 0, 180, nothing)
    cv2.createTrackbar('S_LOW', 'image', 0, 255, nothing)
    cv2.createTrackbar('V_LOW', 'image', 0, 255, nothing)


    # Crea un oggetto VideoCapture per leggere il video
    #cap = cv2.VideoCapture('media/sainz.mp4')

    # Verifica se il video è stato aperto correttamente
    # if not cap.isOpened():
    #     print("Errore nell'apertura del file video")
    #     exit()

    frame = cv2.imread('media/blue.png')
    frame = cv2.resize(frame, (224,224))

    while True:
        # Leggi un frame dal video
        #ret, frame = cap.read()

        # Se il frame non è stato letto correttamente, esci dal ciclo
        # if not ret:
        #     break


        HH= cv2.getTrackbarPos('H_HIGH', 'image')
        SH = cv2.getTrackbarPos('S_HIGH', 'image')
        VH = cv2.getTrackbarPos('V_HIGH', 'image')
        HL= cv2.getTrackbarPos('H_LOW', 'image')
        SL = cv2.getTrackbarPos('S_LOW', 'image')
        VL = cv2.getTrackbarPos('V_LOW', 'image')


        lower = np.uint8([[[HL, SL ,VL]]])  # Example: Red color
        high = np.uint8([[[HH, SH, VH]]])  # Example: Red color
        print('rgb:',lower,',',high)

        # lower = cv2.cvtColor(lower, cv2.COLOR_BGR2HSV)
        # high = cv2.cvtColor(high, cv2.COLOR_BGR2HSV)

        print('hsv:',lower,',',high)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #converto in hsv
        mask = cv2.inRange(frame,lower,high) #maschera nel range dei colori definiti sopra
        #mask = cv2.erode(mask,None,iterations=2) #erosione per migliorare la maschera
        #mask=cv2.dilate(mask,None,iterations=2)

        img[:] = [HH,SH,VH]
        cv2.imshow('Frame', frame)
        cv2.imshow('Hsv', hsv)
        cv2.imshow('Mask',mask)
        cv2.imshow('image', img)


        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == "__main__" :
    main()
