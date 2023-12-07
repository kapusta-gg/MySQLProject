import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QLineEdit, QPushButton, QInputDialog, QErrorMessage, QMessageBox
from PyQt5.QtCore import QPoint, QTimer

from database import create_connection
from objects.buttons import *
from const.constants_main import *
from const.constant_sql_requests import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.last_command = None
        self.data = None
        self.table_names = None
        self.id_row = 0
        self.text_row = ""
        self.isReset = True

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
        self.add_conditions_box.currentIndexChanged.connect(self.set_id_row)

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

        self.update_table_timer = QTimer()
        self.update_table_timer.setInterval(UPDATE_SECONDS * SEC_IN_MILISEC)
        self.update_table_timer.timeout.connect(self.update_table)
        self.update_table_timer.start()

        self.change_table()

    def change_table(self):
        if self.isReset:
            self.add_conditions_box.clear()
            self.add_conditions_line.clear()

        cur = self.db.cursor()
        self.last_command = RU_TABLE_DICT_PROCEDURE[self.table_info.currentText()]
        cur.execute(self.last_command)
        self.table_names = [i[0] for i in cur.description]
        self.table_names.append("Доп. инфо.")
        self.data = cur.fetchall()
        cur.close()
        self.db.reconnect()

        self.add_conditions_box.addItems(self.table_names)
        self.add_items_to_table()

        self.isReset = True

    def add_items_to_table(self):
        self.tableViewer.clear()
        if self.add_conditions_line.text():
            self.text_row = self.add_conditions_line.text()
            if self.text_row[0] == "=":
                data = self.filter_request(self.text_row[1:])
            elif self.text_row[-1] == ";":
                data = [col for col in self.data if self.text_row[:-1] == str(col[self.id_row])]
            else:
                data = [col for col in self.data if self.text_row in str(col[self.id_row])]
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
        temp_btn = QCellButton("Инфо", self.tableViewer.item(i, 0).text(), self)
        self.tableViewer.setCellWidget(i, j, temp_btn)
        temp_btn.clicked.connect(self.open_update_window)

    def open_update_window(self):
        self.update_window = UPDATE_WINDOWS_DICT[self.table_info.currentText()](self.sender().col_id, self.db)
        self.update_window.exec()

    def delete_rows(self):
        self.update_table_timer.stop()
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
        self.update_table_timer.start()

    def update_table(self):
        temp = self.id_row
        self.add_conditions_box.clear()
        self.isReset = False
        self.change_table()
        self.id_row = temp
        self.add_conditions_box.setCurrentIndex(self.id_row)

    def filter_request(self, request):
        cur = self.db.cursor()
        try:
            build_request = FILTER_REQUEST[self.table_info.currentText()] + " " \
                            + COL_NAME_REQUEST[self.table_info.currentText()][self.add_conditions_box.currentIndex()]\
                            + request
            cur.execute(build_request)
            data = cur.fetchall()
        except Exception:
            data = self.data
        finally:
            cur.close()
            self.db.reconnect()
        return data

    def set_id_row(self):
        self.id_row = self.add_conditions_box.currentIndex()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    app.exec_()
