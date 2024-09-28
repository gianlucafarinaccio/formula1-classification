import cv2
import matplotlib.pyplot as plt
import numpy as np



# Definisci la funzione per la correzione gamma
def adjust_gamma(image, gamma=1.0):
    # Costruisci una lookup table per mappare ogni valore di pixel
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    # Applica la mappatura con la lookup table usando cv2.LUT
    return cv2.LUT(image, table)

# Carica l'immagine
image = cv2.imread('media/ombre.png')  # Sostituisci con il percorso della tua immagine
image = cv2.resize(image, (224,224))

# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Applica il filtro Laplaciano
# laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)

# # Somma il Laplaciano all'immagine originale (normalizzazione inclusa)
# enhanced_image = np.float64(gray_image) - laplacian

# # Normalizza i valori per tenerli tra 0 e 255
# enhanced_image = np.clip(enhanced_image, 0, 255)

# # Converti l'immagine di nuovo in uint8
# enhanced_image = np.uint8(enhanced_image)

# # Mostra l'immagine originale e quella enhanced
# cv2.imshow('Original Image', gray_image)
# cv2.imshow('Enhanced Image', enhanced_image)


# shadow_mask = cv2.inRange(gray, 80, 87)


# Converti l'immagine da BGR a HSV
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

# Mostra l'immagine risultante
cv2.imshow('Equalized Image', equalized_image)
cv2.imshow('original', image)

# # Salva l'immagine risultante (opzionale)
# cv2.imwrite('equalized_hue_image.jpg', equalized_image)

# Attendi la chiusura delle finestre
cv2.waitKey(0)
cv2.destroyAllWindows()
