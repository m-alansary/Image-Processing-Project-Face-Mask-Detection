from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2.QtCore import Signal
from PySide2.QtCore import Qt
import csv


class StudentsWidget(QWidget):
    captureImages = Signal(int, str)

    def __init__(self, parent=None):
        super(StudentsWidget, self).__init__(parent)
        self.csvFileName = "Data/students.csv"
        self.tabWidget = QTabWidget(self)
        self.studentsTable = QTableWidget(self)
        self.attendanceTable = QTableWidget(self)
        self.addBtn = QPushButton("Add")
        self.removeBtn = QPushButton("Remove")
        self.saveBtn = QPushButton("Save")
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
        btnsLayout.addStretch()
        studentsWidget.layout().addWidget(self.studentsTable)
        studentsWidget.layout().addLayout(btnsLayout)
        attendanceWidget = QWidget(self)
        attendanceWidget.setLayout(QHBoxLayout())
        attendanceWidget.layout().addWidget(self.attendanceTable)
        self.tabWidget.addTab(studentsWidget, "Students")
        self.tabWidget.addTab(attendanceWidget, "Attendance")
        self.layout().addWidget(self.tabWidget)

        self.studentsTable.verticalHeader().hide()
        self.studentsTable.setColumnCount(4)
        header = self.studentsTable.horizontalHeader()
        for col in range(self.studentsTable.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Stretch)
        self.studentsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Take Images Data"))

    def _start_communication(self):
        self.addBtn.clicked.connect(self._add_btn_clicked)
        self.removeBtn.clicked.connect(self._remove_btn_clicked)
        self.saveBtn.clicked.connect(self._save_btn_clicked)

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

    def _add_btn_at_row(self, row):
        btn = QPushButton("Capture Training Images")
        btn.clicked.connect(lambda: self.capture_images(row))
        self.studentsTable.setCellWidget(row, 3, btn)

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
