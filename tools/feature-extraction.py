import cv2
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

model = VGG16(weights='imagenet', include_top=False)
features = []
labels = []

for img in os.listdir('media/prima-variante'):

	image = cv2.imread('media/prima-variante/'+img)
	image = cv2.resize(image, (224,224))
	img_data = np.expand_dims(image, axis=0)
	img_data = preprocess_input(img_data)
	vgg16_feature = model.predict(img_data)
	features.append(vgg16_feature.flatten())
	labels.append("prima-variante")







X = np.array(features)
y = np.array(labels)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Valutiamo il modello
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')


image = cv2.imread('media/prima-variante/0__445.jpg')
image = cv2.resize(image, (224,224))
img_data = np.expand_dims(image, axis=0)
img_data = preprocess_input(img_data)
features = []
f = model.predict(img_data)
features.append(f.flatten())

features = np.array(features)
predictions = clf.predict(features)
print('prima-variante:')
print(label_encoder.inverse_transform(predictions))



image = cv2.imread('media/parabolica/7__1913.jpg')
image = cv2.resize(image, (224,224))
img_data = np.expand_dims(image, axis=0)
img_data = preprocess_input(img_data)
features = []
f = model.predict(img_data)
features.append(f.flatten())

features = np.array(features)
predictions = clf.predict(features)
print('parabolica:')
print(label_encoder.inverse_transform(predictions))

