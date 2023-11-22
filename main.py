import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import QPoint

from database import create_connection
from constants import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(MAIN_WINDOW_SIZE)

        self.db = create_connection()
        self.cur = self.db.cursor()

        self.table_info = QComboBox(self)
        self.table_info.addItems(TABLES_FOR_INFO)
        self.table_info.move(QPoint(20, 20))
        self.table_info.currentIndexChanged.connect(self.change_table)

        self.tableViewer = QTableWidget(self)
        self.tableViewer.move(200, 100)
        self.tableViewer.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableViewer.setFixedSize(QSize(750, 850))

    def change_table(self):
        table = RU_TABLE_DICT[self.table_info.currentText()]
        self.cur.execute(f"SELECT * FROM {table}")
        data = self.cur.fetchall()

        row_len = len(data[0])
        self.tableViewer.setColumnCount(row_len)
        self.tableViewer.setRowCount(0)
        for i in range(len(data)):
            self.tableViewer.setRowCount(self.tableViewer.rowCount() + 1)
            for j in range(row_len):
                self.tableViewer.setItem(i, j, QTableWidgetItem(str(data[i][j])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    app.exec_()