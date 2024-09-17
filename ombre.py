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


IMAGE_DIM = (224,224)
cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])

# Step 1: Load the image and resize
image = cv2.imread('media/ombre.png')
image = cv2.resize(image, IMAGE_DIM)


# Applica la correzione gamma con un valore gamma (ad esempio, 2.2)
gamma = adjust_gamma(np.copy(image), gamma=1.5)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


cv2.imshow('hsv',hsv)
cv2.imshow('gamma',gamma)
cv2.imshow('image',image)


cv2.waitKey(0)
cv2.destroyAllWindows()