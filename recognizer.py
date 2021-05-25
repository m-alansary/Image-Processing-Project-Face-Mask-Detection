import datetime
import os
import time
import cv2
import pandas as pd
from studentsData import get_student, attend_studnet

threshold = 67 # percentage


def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  
    recognizer.read("Training Images Labels" + os.sep + "Trainner.yml")
    harcascadePath = "haarcascade_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640) 
    cam.set(4, 480) 
    minWidth = 0.1 * cam.get(3)
    minHight = 0.1 * cam.get(4)

    while True:
        ret, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,
                minSize = (int(minWidth), int(minHight)), flags = cv2.CASCADE_SCALE_IMAGE)
        for(p1, p2, p3, p4) in faces:
            cv2.rectangle(image, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2) # BGR
            id, conf = recognizer.predict(gray[p2 : p2 + p4, p1 : p1 + p3])
            imageText = ""
            if 100 - conf > 0:
                name = get_student(id)
                confstr = "  {0}%".format(round(100 - conf))
                imageText = str(id) + "-" + name + " [Pass]"
            else:
                imageText = "\tUnknown\t"
                confstr = "  {0}%".format(round(100 - conf))

            if 100 - conf > threshold:
                ts = time.time()
                attend_studnet(id, ts)

            cv2.putText(image, str(imageText), (p1 + 5, p2 - 5), font, 1, (255, 255, 255), 2)

            if (100 - conf) > threshold:
                cv2.putText(image, str(confstr), (p1 + 5, p2 + p4 - 5), font, 1, (0, 255, 0), 1)
            elif (100 - conf) > 50:
                cv2.putText(image, str(confstr), (p1 + 5, p2 + p4 - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(image, str(confstr), (p1 + 5, p2 + p4 - 5), font, 1, (0, 0, 255), 1)

        cv2.imshow('Attendance', image)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()