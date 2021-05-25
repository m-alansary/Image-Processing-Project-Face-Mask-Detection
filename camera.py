import csv
import cv2
import os
from studentsData import add_student, add_masked_student, currentId


def test_and_detect():
    # Load the cascade
    cascadeFace = cv2.CascadeClassifier('haarcascade_default.xml')

    # Capture the video from webcam
    cap = cv2.VideoCapture(0)

    while True:
        _, image = cap.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = cascadeFace.detectMultiScale(gray, 1.3, 5, minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE)

        for (p1, p2, p3, p4) in faces:
            cv2.rectangle(image, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2) # BGR

        cv2.imshow('Test Camera', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
def capture_training_images(name, id=currentId, path="Training Images"):
    if name.isalpha():
        cam = cv2.VideoCapture(0)
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier("haarcascade_default.xml")
        imageNo = 0

        while(True):
            ret, image = cam.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)

            for (p1, p2, p3, p4) in faces:
                cv2.rectangle(image, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2) # BGR
                imageNo += 1
                cv2.imwrite(path + os.sep + name + "." + str(id) + '.' +
                            str(imageNo) + ".jpg", gray[p2 : p2 + p4, p1 : p1 + p3])
                cv2.imshow('Capturing Image', image)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif imageNo > 100:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        res = "Training data is saved for ID: " + str(id) + " and Name: " + name
        row = [id, name]
        if id == currentId:
            add_student(name)
        else:
            add_masked_student(name)

        return row

