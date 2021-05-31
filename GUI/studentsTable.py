from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2.QtCore import Signal
from PySide2.QtCore import Qt
import csv


class StudentsTable(QWidget):
    captureImages = Signal(int, str)

    def __init__(self, parent=None):
        super(StudentsTable, self).__init__(parent)
        self.csvFileName = "Data/students.csv"
        self.table = QTableWidget(self)
        self.addBtn = QPushButton("Add")
        self.removeBtn = QPushButton("Remove")
        self.saveBtn = QPushButton("Save")
        self._init_ui()
        self._start_communication()
        self.load_csv()

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        btnsLayout = QVBoxLayout(self)
        btnsLayout.addWidget(self.addBtn)
        btnsLayout.addWidget(self.removeBtn)
        btnsLayout.addWidget(self.saveBtn)
        btnsLayout.addStretch()
        self.layout().addWidget(self.table)
        self.layout().addLayout(btnsLayout)

        self.table.verticalHeader().hide()
        self.table.setColumnCount(4)
        header = self.table.horizontalHeader()
        for col in range(self.table.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Stretch)
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Take Images Data"))

    def _start_communication(self):
        self.addBtn.clicked.connect(self._add_btn_clicked)
        self.removeBtn.clicked.connect(self._remove_btn_clicked)
        self.saveBtn.clicked.connect(self._save_btn_clicked)

    def _add_btn_clicked(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        btn = QPushButton("Capture Training Images")
        btn.clicked.connect(lambda: self.capture_images(row))
        self.table.setCellWidget(row, 3, btn)

    def _remove_btn_clicked(self):
        rowsToDelete = []
        for index in self.table.selectedIndexes():
            row = index.row()
            rowsToDelete.append(row)
        rowsToDelete.sort(reverse=True)
        for row in rowsToDelete:
            self.table.removeRow(row)

    def _add_btn_at_row(self, row):
        btn = QPushButton("Capture Training Images")
        btn.clicked.connect(lambda: self.capture_images(row))
        self.table.setCellWidget(row, 3, btn)

    def _save_btn_clicked(self):
        self.write_csv()

    def load_csv(self):
        with open(self.csvFileName) as fileInput:
            row = 0
            for rowData in csv.reader(fileInput, delimiter=','):
                for col in range(len(rowData)):
                    if row == 0:
                        self.table.setHorizontalHeaderItem(col, QTableWidgetItem(rowData[col]))
                    else:
                        if col == 0:
                            self.table.insertRow(row - 1)
                        item = QTableWidgetItem(rowData[col])
                        self.table.setItem(row - 1, col, item)
                if row != 0:
                    self._add_btn_at_row(row - 1)
                row += 1

    def write_csv(self):
        with open(self.csvFileName, "w", newline='') as fileOutput:
            writer = csv.writer(fileOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in range(self.table.rowCount()):
                if row == 0:
                    fields = []
                    for col in range(0, self.table.columnCount() - 1):
                        fields.append(self.table.horizontalHeaderItem(col).text())
                    writer.writerow(fields)
                fields = []
                for col in range(0, self.table.columnCount() - 1):
                    fields.append(self.table.item(row, col).text())
                writer.writerow(fields)

    def capture_images(self, row):
        id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        self.captureImages.emit(id, name)
