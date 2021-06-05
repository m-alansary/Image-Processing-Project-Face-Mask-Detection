import csv
import cv2
import os
import time
from studentsData import add_student, add_masked_student, currentId
from PySide2.QtCore import *
from PySide2.QtGui import *
from studentsData import get_student, attend_studnet

threshold = 67  # percentage


class Camera(QThread):
    updateImage = Signal(str, QImage, dict)  # Title, image

    def set_method(self, name, params={}):
        self.name = name
        self.params = params

    def run(self):
        self.isActive = True
        if self.name == "test_and_detect":
            self.test_and_detect()
        elif self.name == "capture_training_images":
            self.capture_training_images(self.params["name"], self.params["id"])
        elif self.name == "recognize_attendence":
            self.recognize_attendence(self.params["students"])

    def test_and_detect(self):
        # Load the cascade
        cascadeFace = cv2.CascadeClassifier('haarcascade_default.xml')

        # Capture the video from webcam
        cap = cv2.VideoCapture(0)

        while self.isActive:
            _, image = cap.read()

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = cascadeFace.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for (p1, p2, p3, p4) in faces:
                cv2.rectangle(image, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2)  # BGR

            self.emit_image('Test Camera', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.emit_image('', None)
        cap.release()
        cv2.destroyAllWindows()

    def capture_training_images(self, name: str, id: int, path="Training Images"):
        if name.replace(" ", "").isalpha():
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier("haarcascade_default.xml")
            imageNo = 0

            while self.isActive:
                ret, image = cam.read()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

                for (p1, p2, p3, p4) in faces:
                    cv2.rectangle(image, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2)  # BGR
                    imageNo += 1
                    cv2.imwrite(path + os.sep + name + "." + str(id) + '.' +
                                str(imageNo) + ".jpg", gray[p2: p2 + p4, p1: p1 + p3])

                self.emit_image("Capturing Training Images", image, {"id": str(id), "name": name})

                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif imageNo > 100:
                    break

            cam.release()
            cv2.destroyAllWindows()
            self.emit_image('', None)

            row = [id, name]

            return row

    def recognize_attendence(self, students: dict):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("Training Images Labels" + os.sep + "Trainner.yml")
        # recognizerMask = cv2.face.LBPHFaceRecognizer_create()
        # recognizerMask.read("Training Images Mask Labels" + os.sep + "Trainner.yml")
        harcascadePath = "haarcascade_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        minWidth = 0.1 * cam.get(3)
        minHight = 0.1 * cam.get(4)

        while self.isActive:
            data = {}
            ret, image = cam.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5,
                                                 minSize=(int(minWidth), int(minHight)), flags=cv2.CASCADE_SCALE_IMAGE)
            masked = False
            for (p1, p2, p3, p4) in faces:
                cv2.rectangle(image, (p1, p2), (p1 + p3, p2 + p4), (0, 0, 255), 2)  # BGR
                # id, conf = recognizerMask.predict(gray[p2 : p2 + p4, p1 : p1 + p3])
                # if 100 - conf <= 65:
                id, conf = recognizer.predict(gray[p2: p2 + p4, p1: p1 + p3])
                # else:
                #     masked = True
                imageText = ""
                if 100 - conf > 0:
                    name = students[id]
                    confstr = "  {0}%".format(round(100 - conf))
                    imageText = str(id) + "-" + name + " [Pass]"
                    data["id"] = str(id)
                    data["name"] = name
                    if masked:
                        imageText += " [Masked]"
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

            self.emit_image("Taking Attendance", image, data)
            if cv2.waitKey(1) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()
        self.emit_image('', None)

    def emit_image(self, title, image, data={}):
        if image is not None:
            height, width, bytesPerComponent = image.shape
            bytesPerLine = bytesPerComponent * width
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            imageConversion = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # qtImage = imageConversion.scaled(640, 480, Qt.KeepAspectRatio)
            self.updateImage.emit(title, imageConversion, data)
        else:
            self.updateImage.emit('', QImage(), data)

    def stop(self):
        self.emit_image('', None)
        self.isActive = False
        self.quit()

