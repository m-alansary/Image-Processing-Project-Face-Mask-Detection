import os
import time
import cv2
import numpy as np
from PIL import Image
from threading import Thread


def get_data(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        image = Image.open(imagePath).convert('L')
        imageNp = np.array(image, 'uint8')
        Id = int(float(os.path.split(imagePath)[-1].split(".")[1]))
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = get_data("Training Images")
    Thread(target = recognizer.train(faces, np.array(Id))).start()
    recognizer.save("Training Images Labels" + os.sep + "Trainner.yml")
