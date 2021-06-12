from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2.QtCore import Signal
from PySide2.QtCore import Qt
import csv
from modelTraining import train_model
from recognizer import recognize_attendence


class StudentsWidget(QWidget):
    captureImages = Signal(int, str)
    takeAttendance = Signal(dict)
    endAttendance = Signal()

    def __init__(self, parent=None):
        super(StudentsWidget, self).__init__(parent)
        self.csvFileName = "Data/students.csv"
        self.tabWidget = QTabWidget(self)
        self.studentsTable = QTableWidget(self)
        self.attendanceTable = QTableWidget(self)
        self.addBtn = QPushButton("Add")
        self.removeBtn = QPushButton("Remove")
        self.saveBtn = QPushButton("Save")
        self.trainBtn = QPushButton("Train Model")
        self.attendanceBtn = QPushButton("Take Attendance")
        self._init_ui()
        self._start_communication()
        self.load_csv()

    def _init_ui(self):
        studentsWidget = QWidget(self)
        studentsWidget.setLayout(QHBoxLayout(self))
        self.setLayout(QHBoxLayout())
        btnsLayout = QVBoxLayout(self)
        btnsLayout.addWidget(self.addBtn)
        btnsLayout.addWidget(self.removeBtn)
        btnsLayout.addWidget(self.saveBtn)
        btnsLayout.addWidget(self.trainBtn)
        btnsLayout.addStretch()
        studentsWidget.layout().addWidget(self.studentsTable)
        studentsWidget.layout().addLayout(btnsLayout)
        attendanceWidget = QWidget(self)
        attendanceWidget.setLayout(QHBoxLayout())
        attendanceWidget.layout().addWidget(self.attendanceTable)
        btnsLayout = QVBoxLayout(self)
        btnsLayout.addWidget(self.attendanceBtn)
        btnsLayout.addStretch()
        attendanceWidget.layout().addLayout(btnsLayout)
        self.tabWidget.addTab(studentsWidget, "Students")
        self.tabWidget.addTab(attendanceWidget, "Attendance")
        self.layout().addWidget(self.tabWidget)

        self.studentsTable.setColumnCount(4)
        header = self.studentsTable.horizontalHeader()
        for col in range(self.studentsTable.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Stretch)
        self.studentsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Take Images Data"))
        self.attendanceTable.setColumnCount(2)
        self.attendanceTable.setHorizontalHeaderLabels(["ID", "Name"])
        header = self.attendanceTable.horizontalHeader()
        for col in range(self.attendanceTable.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Stretch)

    def _start_communication(self):
        self.addBtn.clicked.connect(self._add_btn_clicked)
        self.removeBtn.clicked.connect(self._remove_btn_clicked)
        self.saveBtn.clicked.connect(self._save_btn_clicked)
        self.trainBtn.clicked.connect(self._train_btn_clicked)
        self.attendanceBtn.clicked.connect(self.take_attendance)

    def _add_btn_clicked(self):
        row = self.studentsTable.rowCount()
        self.studentsTable.insertRow(row)
        btn = QPushButton("Capture Training Images")
        btn.clicked.connect(lambda: self.capture_images(row))
        self.studentsTable.setCellWidget(row, 3, btn)

    def _remove_btn_clicked(self):
        rowsToDelete = []
        for index in self.studentsTable.selectedIndexes():
            row = index.row()
            rowsToDelete.append(row)
        rowsToDelete.sort(reverse=True)
        for row in rowsToDelete:
            self.studentsTable.removeRow(row)

    def _train_btn_clicked(self):
        self.trainBtn.setEnabled(False)
        self.trainBtn.setText("Training...")
        train_model()
        self.trainBtn.setText("Train Model")
        self.trainBtn.setEnabled(True)

    def _add_btn_at_row(self, row):
        btn = QPushButton("Capture Training Images")
        btn.clicked.connect(lambda: self.capture_images(row))
        self.studentsTable.setCellWidget(row, 3, btn)

    def take_attendance(self):
        if self.attendanceBtn.text() == "Take Attendance":
            students = self.get_students()
            self.takeAttendance.emit(students)
            self.attendanceBtn.setText("Finish")
        else:
            self.endAttendance.emit()
            self.attendanceBtn.setText("Take Attendance")

    def get_students(self):
        students = {}
        for row in range(self.studentsTable.rowCount()):
            students[int(self.studentsTable.item(row, 0).text())] = self.studentsTable.item(row, 1).text()
        return students

    def set_attendance(self, data):
        self.attendanceTable.setRowCount(0)
        row = 0
        for id in data:
            self.attendanceTable.insertRow(row)
            item = QTableWidgetItem(id)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.attendanceTable.setItem(row, 0, item)
            item = QTableWidgetItem(data[id])
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.attendanceTable.setItem(row, 1, item)

    def _save_btn_clicked(self):
        self.write_csv()

    def load_csv(self):
        with open(self.csvFileName) as fileInput:
            row = 0
            for rowData in csv.reader(fileInput, delimiter=','):
                for col in range(len(rowData)):
                    if row == 0:
                        self.studentsTable.setHorizontalHeaderItem(col, QTableWidgetItem(rowData[col]))
                    else:
                        if col == 0:
                            self.studentsTable.insertRow(row - 1)
                        item = QTableWidgetItem(rowData[col])
                        self.studentsTable.setItem(row - 1, col, item)
                if row != 0:
                    self._add_btn_at_row(row - 1)
                row += 1

    def write_csv(self):
        with open(self.csvFileName, "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in range(self.studentsTable.rowCount()):
                if row == 0:
                    fields = []
                    for col in range(0, self.studentsTable.columnCount() - 1):
                        fields.append(self.studentsTable.horizontalHeaderItem(col).text())
                    writer.writerow(fields)
                fields = []
                for col in range(0, self.studentsTable.columnCount() - 1):
                    fields.append(self.studentsTable.item(row, col).text())
                writer.writerow(fields)

    def capture_images(self, row):
        id = int(self.studentsTable.item(row, 0).text())
        name = self.studentsTable.item(row, 1).text()
        self.captureImages.emit(id, name)
