import csv
import cv2
import os
from studentsData import add_student, add_masked_student, currentId
from PySide2.QtCore import *
from PySide2.QtGui import *


class Camera(QThread):
    updateImage = Signal(str, QImage)  # Title, image

    def set_method(self, name, params={}):
        self.name = name
        self.params = params

    def run(self):
        self.isActive = True
        if self.name == "test_and_detect":
            self.test_and_detect()
        elif self.name == "capture_training_images":
            self.capture_training_images(self.params["name"], self.params["id"])

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

                self.emit_image("Capturing Training Images", image)

                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif imageNo > 100:
                    break

            cam.release()
            cv2.destroyAllWindows()
            self.emit_image('', None)

            row = [id, name]
            if id == currentId:
                add_student(name)
            else:
                add_masked_student(name)

            return row

    def emit_image(self, title, image):
        if image is not None:
            height, width, bytesPerComponent = image.shape
            bytesPerLine = bytesPerComponent * width
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            imageConversion = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
            # qtImage = imageConversion.scaled(640, 480, Qt.KeepAspectRatio)
            self.updateImage.emit(title, imageConversion)
        else:
            self.updateImage.emit('', QImage())

    def stop(self):
        self.isActive = False
        self.quit()

