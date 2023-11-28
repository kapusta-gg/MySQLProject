import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView,\
    QLineEdit, QPushButton, QInputDialog, QErrorMessage, QMessageBox
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

        self.add_conditions_line = QLineEdit(self)
        self.add_conditions_line.move(QPoint(300, 70))
        self.add_conditions_line.resize(QSize(650, 30))
        self.add_conditions_line.textChanged.connect(self.add_items_to_table)

        self.add_conditions_box = QComboBox(self)
        self.add_conditions_box.move(QPoint(200, 70))
        self.add_conditions_box.currentIndexChanged.connect(self.add_items_to_table)
        self.add_conditions_box.currentIndexChanged.connect(self.add_conditions_line.clear)

        self.tableViewer = QTableWidget(self)
        self.tableViewer.move(QPoint(200, 100))
        self.tableViewer.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableViewer.setFixedSize(QSize(750, 850))

        self.delete_rows_btn = QPushButton("Удалить все\nотображаемые записи", self)
        self.delete_rows_btn.resize(QSize(140, 60))
        self.delete_rows_btn.move(QPoint(30, 100))
        self.delete_rows_btn.clicked.connect(self.delete_rows)

        self.add_col = QPushButton("Добавить запись", self)
        self.add_col.resize(QSize(140, 60))
        self.add_col.move(QPoint(30, 160))

        self.change_table()

    def change_table(self):
        self.add_conditions_box.clear()
        self.add_conditions_line.clear()

        cur = self.db.cursor()
        self.last_command = RU_TABLE_DICT_PROCEDURE[self.table_info.currentText()]
        cur.execute(self.last_command)
        self.table_names = [i[0] for i in cur.description]
        self.table_names.append("Доп. инфо.")
        self.data = cur.fetchall()

        self.add_conditions_box.addItems(self.table_names)
        self.add_items_to_table()

        cur.close()
        self.db.reconnect()

    def add_items_to_table(self):
        self.tableViewer.clear()
        if self.add_conditions_line.text():
            id_row = self.add_conditions_box.currentIndex()
            if self.add_conditions_line.text()[-1] == ";":
                data = [col for col in self.data if self.add_conditions_line.text()[:-1] == str(col[id_row])]
            else:
                data = [col for col in self.data if self.add_conditions_line.text() in str(col[id_row])]
        else:
            data = self.data
        row_len = len(self.table_names)
        self.tableViewer.setColumnCount(row_len)
        self.tableViewer.setRowCount(0)
        for i in range(len(data)):
            self.tableViewer.setRowCount(self.tableViewer.rowCount() + 1)
            for j in range(row_len - 1):
                self.tableViewer.setItem(i, j, QTableWidgetItem(str(data[i][j])))
            self.add_cell_button(i, row_len - 1)
        self.tableViewer.setHorizontalHeaderLabels(self.table_names)
        self.tableViewer.resizeColumnsToContents()

    def add_cell_button(self, i, j):
        temp_btn = QPushButton("Инфо", self)

        self.tableViewer.setCellWidget(i, j, temp_btn)

    def delete_rows(self):
        text, ok = QInputDialog().getText(self, "Введите пароль", "Введите пароль администратора")
        if ok and text == ADMIN_PASSWORD:
            indexes = [self.tableViewer.item(i, 0).text() for i in range(self.tableViewer.rowCount())]
            self.accept_delete(indexes)
        else:
            QErrorMessage(self).showMessage("Отказано в доступе")

    def accept_delete(self, indexes):
        accept_dlg = QMessageBox(self)
        accept_dlg.setWindowTitle("Подтверждение")
        accept_dlg.setText(f"Вы точно хотите удалить из таблицы '{self.table_info.currentText()}'"
                           f" {len(indexes)} записей?")
        accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        but = accept_dlg.exec()

        if but == QMessageBox.Yes:
            cur = self.db.cursor()
            cur.execute(f"DELETE FROM {DATABASE_TABLES[self.table_info.currentText()]}"
                        f" WHERE {COL_ID_NAME_DATABASE_TABLES[self.table_info.currentText()]} IN "
                        f" " + "(" + ", ".join(indexes) + ")")
            self.db.commit()
            cur.close()
            self.db.reconnect()
            self.change_table()

            ok_dlg = QMessageBox(self)
            ok_dlg.setText(f"Успешно удалено {len(indexes)} записей из таблицы '{self.table_info.currentText()}'")
            ok_dlg.setStandardButtons(QMessageBox.Ok)
            ok_dlg.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    app.exec_()