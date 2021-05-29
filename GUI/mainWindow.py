import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import cv2
from camera import Camera


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.title = QLabel()
        self.image = QLabel()
        self.camera = Camera()
        self.camera.set_method("capture", {"name": "Ansary"})
        self.camera.start()
        self.camera.updateImage.connect(self.update_image)
        self._init_ui()
        self.setMinimumSize(640, 480)

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.title)
        self.layout().addWidget(self.image)

    def update_image(self, title, image):
        self.title.setText(title)
        self.image.setPixmap(QPixmap.fromImage(image))



