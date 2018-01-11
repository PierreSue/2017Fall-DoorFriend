import cv2
import os
import numpy as np
import pickle
#subjects = ['', 'Pierre', 'Monmon', 'Chihwei']

subjects = ['', 'Pierre', 'Monmon']

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)

    label, confidence = face_recognizer.predict(face)
    label_text = 'error!'
    if confidence < 80:
        label_text = subjects[label]
        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1]-5)
    else:
        draw_rectangle(img, rect)
        draw_text(img, 'error!!', rect[0], rect[1]-5)
    return img, label_text

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if (len(faces) == 0):
        return None, None

    print(len(faces))
 
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    
    faces = []
 
    labels = []
    for dir_name in dirs:
        if not dir_name.startswith('s'):
            continue;
        label = int(dir_name.replace('s', ''))
        subject_dir_path = data_folder_path + '/' + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith('.'):
                continue;
           
            image_path = subject_dir_path + '/' + image_name

            print('Read {}'.format(image_path))
            image = cv2.imread(image_path)
            face, rect = detect_face(image)
   
            if face is not None:
                faces.append(face)
                labels.append(label)
            else:
                print('{} has no face!'.format(image_path))

    return faces, labels

faces, labels = prepare_training_data('data/training-data')
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

test_img1 = cv2.imread('data/test-data/test1.jpg')
test_img2 = cv2.imread('data/test-data/test2.jpg')
test_img3 = cv2.imread('data/test-data/test3.jpg')
test_img4 = cv2.imread('data/test-data/test4.jpg')
predicted_img1, label1 = predict(test_img1)
predicted_img2, label2 = predict(test_img2)
predicted_img3, label3 = predict(test_img3)
predicted_img4, label4 = predict(test_img4)
print('Prediction complete')
print('1: {}, 2: {}, 3: {}, 4: {}'.format(label1, label2, label3, label4))

print('Saving model')
face_recognizer.write('data/recognizer.xml')
pickle.dump(subjects, open('data/labels.pkl', 'wb'))