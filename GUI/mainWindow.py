from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from GUI.cameraChart import CameraChart
from GUI.studentsTable import StudentsTable


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cameraChart = CameraChart(self)
        self.tabWidget = QTabWidget(self)
        self.studentsTable = StudentsTable(self)
        self._init_ui()
        self._start_communication()

    def _init_ui(self):
        widget = QWidget()
        self.tabWidget.addTab(self.studentsTable, "Students")
        self.tabWidget.addTab(QWidget(), "Attendance")
        widget.setLayout(QHBoxLayout())
        widget.layout().addWidget(self.cameraChart)
        widget.layout().addWidget(self.tabWidget)
        self.setCentralWidget(widget)

    def _start_communication(self):
        self.studentsTable.captureImages.connect(self.capture_images)

    def capture_images(self, id: int, name: str):
        self.cameraChart.capture_images(id, name)



