
import cv2
import os
import picamera
from time import sleep
import numpy as np

subjects = ["", "Pierre", "Monmon", "Chihwei", "Professor"]
camera = picamera.PiCamera()



def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)

    if face is None:
        return None, "no face"

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read("recognizer.xml")
    label, confidence = face_recognizer.predict(face)
    label_text = "error"
    if confidence < 80 :
        label_text = subjects[label]
        draw_rectangle(img, rect)
    else:
        draw_rectangle(img, rect)
        draw_text(img, "error!!", rect[0], rect[1]-5)
    return img,label_text
def draw_rectangle(img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
def draw_text(img, text, x, y):
     cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)



def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[-1]
    return gray[y:y+w, x:x+h], faces[-1]

while True:
    camera.capture('image11.jpg')

    test_img1 = cv2.imread("image11.jpg")
    test_img1 = cv2.resize(test_img1, (0,0), fx=0.5, fy=0.5)
    predicted_img1 = predict(test_img1)
    predicted_img1, label1 = predict(test_img1) 
    print("1: {}".format(label1))
    sleep(1)
