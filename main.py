import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView,\
    QLineEdit
from PyQt5.QtCore import QPoint

from database import create_connection
from constants import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.last_command = None
        self.data = None
        self.table_names = None

        self.setFixedSize(MAIN_WINDOW_SIZE)

        self.db = create_connection()

        self.table_info = QComboBox(self)
        self.table_info.addItems(TABLES_FOR_INFO)
        self.table_info.move(QPoint(20, 20))
        self.table_info.currentIndexChanged.connect(self.change_table)

        self.add_conditions_box = QComboBox(self)
        self.add_conditions_box.move(QPoint(200, 70))

        self.add_conditions_line = QLineEdit(self)
        self.add_conditions_line.move(QPoint(300, 70))
        self.add_conditions_line.resize(QSize(650, 30))

        self.tableViewer = QTableWidget(self)
        self.tableViewer.move(QPoint(200, 100))
        self.tableViewer.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableViewer.setFixedSize(QSize(750, 850))

        self.change_table()

    def change_table(self):
        self.add_conditions_box.clear()
        self.add_conditions_line.clear()

        cur = self.db.cursor()
        self.last_command = RU_TABLE_DICT_PROCEDURE[self.table_info.currentText()]
        cur.execute(self.last_command)
        self.table_names = [i[0] for i in cur.description]
        self.data = cur.fetchall()

        self.add_conditions_box.addItems(self.table_names)
        self.add_items_to_table()

        cur.close()
        self.db.reconnect()

    def add_items_to_table(self):
        self.tableViewer.clear()
        row_len = len(self.table_names)
        self.tableViewer.setColumnCount(row_len)
        self.tableViewer.setRowCount(0)

        for i in range(len(self.data)):
            self.tableViewer.setRowCount(self.tableViewer.rowCount() + 1)
            for j in range(row_len):
                self.tableViewer.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

        self.tableViewer.setHorizontalHeaderLabels(self.table_names)
        self.tableViewer.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    app.exec_()