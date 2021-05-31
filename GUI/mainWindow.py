from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from GUI.cameraChart import CameraChart
from GUI.studentsWidget import StudentsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cameraChart = CameraChart(self)
        self.studentsTable = StudentsWidget(self)
        self._init_ui()
        self._start_communication()

    def _init_ui(self):
        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        widget.layout().addWidget(self.cameraChart)
        widget.layout().addWidget(self.studentsTable)
        self.setCentralWidget(widget)

    def _start_communication(self):
        self.studentsTable.captureImages.connect(self.capture_images)

    def capture_images(self, id: int, name: str):
        self.cameraChart.capture_images(id, name)



