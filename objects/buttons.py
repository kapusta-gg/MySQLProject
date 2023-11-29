import sys

from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication


class QCellButton(QPushButton):
    def __init__(self, text, col_id, parent=None):
        super().__init__(text, parent)
        self.col_id = col_id


if __name__ == "__main__":
    class MyApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.but = QCellButton("Test", 1, self)

    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec_()