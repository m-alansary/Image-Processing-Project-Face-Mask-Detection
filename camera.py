import csv
import cv2
import os

currentId = 0


def test_and_detect():
    # Load the cascade
    cascadeFace = cv2.CascadeClassifier('haarcascade_default.xml')

    # Capture the video from webcam
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = cascadeFace.detectMultiScale(gray, 1.3, 5, minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE)

        for (p1, p2, p3, p4) in faces:
            cv2.rectangle(img, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2) # BGR

        cv2.imshow('Test Camera', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def capture_training_images(name):
    global currentId
    id = str(currentId)
    currentId += 1

    if name.isalpha():
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier("haarcascade_default.xml")
        imageNo = 0

        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)

            for (p1, p2, p3, p4) in faces:
                cv2.rectangle(img, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2) # BGR
                imageNo += 1
                cv2.imwrite("Training Images" + os.sep + name + "." + id + '.' +
                            str(imageNo) + ".jpg", gray[p2 : p2 + p4, p1 : p1 + p3])
                cv2.imshow('Capturing Image', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif imageNo > 100:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        res = "Training data is saved for ID: " + id + " and Name: " + name
        row = [id, name]
        return row

