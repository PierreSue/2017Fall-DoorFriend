import cv2
import os
import picamera
from time import sleep
import numpy as np
import socket
import RPi.GPIO as GPIO
import pickle

OPEN_PIN = 27
ALARM_PIN = 17
NOTIFY_PIN = 22
BUSY_PIN = 4

KITCHEN_HOST = '192.168.1.199'
KITCHEN_PORT = 5000

subjects = pickle.load(open('data/labels.pkl', 'rb'))
print(subjects)
camera = picamera.PiCamera()

GPIO.setmode(GPIO.BCM)
GPIO.setup(OPEN_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(ALARM_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(NOTIFY_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUSY_PIN, GPIO.OUT, initial=GPIO.HIGH)

def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)

    if face is None:
        return None, "no face", img

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read("data/recognizer.xml")
    label, confidence = face_recognizer.predict(face)
    label_text = "not in the training set"
    if confidence < 80 :
        label_text = subjects[label]
        draw_rectangle(img, rect)
    else:
        draw_rectangle(img, rect)
        draw_text(img, "error!!", rect[0], rect[1]-5)
    return img,label_text,face
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
    camera.capture('data/tmpimage.jpg', resize=(800, 600))
    test_img1 = cv2.imread('data/tmpimage.jpg')
    predicted_img1, label1, face1 = predict(test_img1)
    #cv2.imshow("recog", face1)
    #cv2.waitKey(1000)
    if (label1 != "no face" and label1 != "not in the training set"):
        GPIO.output(NOTIFY_PIN, 0)
        print("1: {}".format(label1))
        os.system('arecord -f cd -t wav -c 1 -D plughw:1,0 -d 5 testdata.wav')
        GPIO.output(NOTIFY_PIN, 1)
        GPIO.output(BUSY_PIN, 0)
        code = os.system('bash /home/pi/final/run.sh ' + label1)
        code = code >> 8
        print('code={}'.format(code))
        good = False
        if code == 1:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((KITCHEN_HOST, KITCHEN_PORT))
                s.send('{}\n'.format(label1).encode('utf-8'))
                rx = s.recv(1024).decode('utf-8').rstrip('\r\n')
                if rx == '1':
                    good = True
                s.close()
            except:
                pass
        GPIO.output(BUSY_PIN, 1)
        if good:
            GPIO.output(OPEN_PIN, 0)
            sleep(0.5)
            GPIO.output(OPEN_PIN, 1)
        else:
            GPIO.output(ALARM_PIN, 0)
            sleep(0.5)
            GPIO.output(ALARM_PIN, 1)
        sleep(1)
    else:
        print(label1)
        sleep(1)
