import cv2
import os
import numpy as np
import pickle
import time
import sys
import picamera

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if (len(faces) == 0):
        return None, None

    print(len(faces))
 
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

camera = picamera.PiCamera()

labels = pickle.load(open('data/labels.pkl', 'rb'))

new_label = raw_input('> Enter your name: ')

if new_label in labels:
    print('Name exists!')
    sys.exit(0)

new_idx = len(labels)
labels.append(new_label)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('data/recognizer.xml')

train_imgs = []
train_lbls = []

for i in range(5):
    print('Image #{}'.format(i))
    success = False
    while not success:
        print('Capturing')
        camera.capture('data/tmpimage.jpg', resize=(800, 600))
        image = cv2.imread('data/tmpimage.jpg')
        face, rect = detect_face(image)
        if face is not None:
            train_lbls.append(new_idx)
            train_imgs.append(face)
            success = True
        else:
            print('Failed, please retry!')
        time.sleep(0.5)

print('Updating model..')
face_recognizer.update(train_imgs, np.array(train_lbls))
print('Saving data..')
face_recognizer.write('data/recognizer.xml')
pickle.dump(labels, open('data/labels.pkl', 'wb'))

print('Completed!')