from PySide2.QtGui import *
from PySide2.QtWidgets import *


class CameraChart(QWidget):
    def __init__(self, parent=None):
        super(CameraChart, self).__init__(parent)
        self.title = QLabel(self)
        self.image = QLabel(self)
        self.infoTable = QTableWidget(self)
        self.camera = None
        # self.camera.set_method("capture", {"name": "Ansary"})
        # self.camera.start()
        # self.camera.updateImage.connect(self.update_image)
        self._init_ui()
        self._init_style()

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.title)
        self.layout().addWidget(self.image)
        self.layout().addWidget(self.infoTable)

    def _init_style(self):
        self.image.setFixedSize(640, 480)
        self.setFixedWidth(640)

    def update_image(self, title, image):
        self.title.setText(title)
        self.image.setPixmap(QPixmap.fromImage(image))

