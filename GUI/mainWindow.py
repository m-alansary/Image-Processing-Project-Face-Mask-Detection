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

    def _init_ui(self):
        widget = QWidget()
        self.tabWidget.addTab(self.studentsTable, "Students")
        self.tabWidget.addTab(QWidget(), "Attendance")
        widget.setLayout(QHBoxLayout())
        widget.layout().addWidget(self.cameraChart)
        widget.layout().addWidget(self.tabWidget)
        self.setCentralWidget(widget)



