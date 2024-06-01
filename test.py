import os
import cv2
import numpy as np
from tensorflow import keras
from keras.preprocessing import image
from keras.preprocessing.image import load_img, img_to_array 
from keras.models import  load_model
import calendar
from datetime import datetime
import openpyxl
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import csv
import time

def write_to_csvhead(file_path):
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #time.sleep(1)
        # Write header
        csv_writer.writerow(['timestamp', 'Intensity', 'emotion'])



def write_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #time.sleep(1)
        # Write header
            #csv_writer.writerow(['timestamp', 'Intensity', 'emotion'])
        # Write data
        csv_writer.writerows(data)

# load model
model = load_model("best_model.h5")  

face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
file_path1='test.csv'
write_to_csvhead(file_path1)
while True:

    ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
    if not ret:
        continue
    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    for (x, y, w, h) in faces_detected:
        cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
        roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
        roi_gray = cv2.resize(roi_gray, (224, 224))
        img_pixels = image.img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255

        predictions = model.predict(img_pixels)
       
        # find max indexed array
        max_index = np.argmax(predictions[0])

        emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
        predicted_emotion = emotions[max_index]

        # Your recursive data structure (example)
        data_to_write = [
            (datetime.now(), np.max(predictions[0]), predicted_emotion)
        ]
        # Specify the file path
        file_path = 'test.csv'
        # Call the function to write data to the CSV file
        write_to_csv(file_path, data_to_write)

        cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('Facial emotion analysis ', resized_img)

    if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
        break


cap.release()
cv2.destroyAllWindows