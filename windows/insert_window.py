import sys
import re
import datetime

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget, QDateEdit, QApplication, \
    QMessageBox
from PyQt5.Qt import QPoint
from abc import abstractmethod

from const.constants_insert_window import *
from const.constant_sql_requests import STUDENTS_TO_GROUP_REQUEST


class InsertWindow(QDialog):
    def __init__(self, bd):
        super().__init__()
        self.setFixedSize(WINDOW_SIZE)
        self.bd = bd

    @abstractmethod
    def insert(self):
        pass


class InsertHumanWindow(InsertWindow):
    def __init__(self, bd):
        super().__init__(bd)
        self.is_passport = False
        self.is_name = self.is_surname = self.is_email = False

        self.name_l = QLabel("Имя:", self)
        self.name_l.move(QPoint(30, 30))
        self.name_i = QLineEdit(self)
        self.name_i.resize(QSize(100, 20))
        self.name_i.move(QPoint(70, 30))

        self.surname_l = QLabel("Фамилия:", self)
        self.surname_l.move(QPoint(180, 30))
        self.surname_i = QLineEdit(self)
        self.surname_i.resize(QSize(100, 20))
        self.surname_i.move(QPoint(240, 30))

        self.email_l = QLabel("Почта:", self)
        self.email_l.move(QPoint(30, 50))
        self.email_i = QLineEdit(self)
        self.email_i.resize(QSize(100, 20))
        self.email_i.move(QPoint(70, 50))

        self.name_i.textChanged.connect(self.filter_for_names)
        self.surname_i.textChanged.connect(self.filter_for_names)
        self.email_i.textChanged.connect(self.filter_for_email)

        self.ok_btn = QPushButton("OK", self)
        self.ok_btn.resize(QSize(60, 40))
        self.ok_btn.move(QPoint(200, 450))
        self.ok_btn.setVisible(False)
        self.ok_btn.clicked.connect(self.insert)

        self.close_btn = QPushButton("Отмена", self)
        self.close_btn.resize(QSize(60, 40))
        self.close_btn.move(QPoint(280, 450))
        self.close_btn.clicked.connect(self.close)

        self.passport_btn = QPushButton("Добавить паспорт", self)
        self.passport_btn.move(QPoint(30, 80))
        self.passport_btn.setVisible(False)

    def filter_for_email(self):
        if not re.findall(r"[a-zA-Z0-9.]+[@]+[a-z]+[.]+[a-z]+", self.sender().text()):
            self.is_email = False
            self.sender().setStyleSheet("border :1px solid ; border-color : red;")
        else:
            self.is_email = True
            self.sender().setStyleSheet("border :1px solid ; border-color : green;")

    @abstractmethod
    def open_passport_window(self):
        pass

    @abstractmethod
    def set_visible_remove_btn(self):
        pass

    def filter_for_names(self):
        text = "".join(re.findall(r"[а-яА-ЯёЁ]", self.sender().text()))[:20].capitalize()
        if text:
            self.sender().setText("".join(re.findall(r"[а-яА-ЯёЁ]", self.sender().text()))[:20].capitalize())
            self.sender().setStyleSheet("border :1px solid ; border-color : green;")
            if self.sender() == self.name_i:
                self.is_name = True
            else:
                self.is_surname = True
        else:
            self.sender().setStyleSheet("border :1px solid ; border-color : red;")
            self.is_name = self.is_surname = False
        if self.name_i.text() and self.surname_i.text():
            self.set_visible_btn()

    def set_visible_btn(self):
        if self.name_i.text() and self.surname_i.text():
            is_visible = True
        else:
            is_visible = False
        self.passport_btn.setVisible(is_visible)
        self.birth_btn.setVisible(is_visible)

    class InsertPassport(QDialog):
        def __init__(self, birthday):
            self.birthday = birthday
            super().__init__()
            self.check1 = self.check2 = self.check3 = self.check4 = self.check5 = False
            self.setFixedSize(DOC_WINDOW_SIZE)
            self.series_l = QLabel("Серия:", self)
            self.series_l.move(QPoint(30, 30))
            self.series_i = QLineEdit(self)
            self.series_i.resize(QSize(100, 20))
            self.series_i.move(QPoint(70, 30))
            self.series_i.textChanged.connect(self.check_series)
            self.series_i.textChanged.connect(self.check_all)

            self.num_l = QLabel("Номер:", self)
            self.num_l.move(QPoint(180, 30))
            self.num_i = QLineEdit(self)
            self.num_i.resize(QSize(100, 20))
            self.num_i.move(QPoint(220, 30))
            self.num_i.textChanged.connect(self.check_code_and_num)
            self.num_i.textChanged.connect(self.check_all)

            self.code_l = QLabel("Код подразделения:", self)
            self.code_l.move(QPoint(30, 50))
            self.code_i = QLineEdit(self)
            self.code_i.resize(QSize(100, 20))
            self.code_i.move(QPoint(140, 50))
            self.code_i.textChanged.connect(self.check_code_and_num)
            self.code_i.textChanged.connect(self.check_all)

            self.agency_l = QLabel("Структурное подразделение:", self)
            self.agency_l.move(QPoint(30, 80))
            self.agency_i = QLineEdit(self)
            self.agency_i.resize(QSize(250, 20))
            self.agency_i.move(QPoint(190, 80))
            self.agency_i.textChanged.connect(self.check_agency)
            self.agency_i.textChanged.connect(self.check_all)

            self.birth_l = QLabel("Дата рождения:", self)
            self.birth_l.move(QPoint(30, 110))
            self.birth_i = QDateEdit(self)
            self.birth_i.move(QPoint(120, 110))
            self.birth_i.dateChanged.connect(self.check_date)
            self.birth_i.dateChanged.connect(self.check_all)

            self.issue_l = QLabel("Дата выдачи:", self)
            self.issue_l.move(QPoint(210, 110))
            self.issue_i = QDateEdit(self)
            self.issue_i.move(QPoint(290, 110))
            self.issue_i.dateChanged.connect(self.check_date)
            self.issue_i.dateChanged.connect(self.check_all)

            self.ok_btn = QPushButton("OK", self)
            self.ok_btn.resize(QSize(60, 40))
            self.ok_btn.move(QPoint(200, 250))
            self.ok_btn.setVisible(False)
            self.ok_btn.clicked.connect(self.add)

            self.close_btn = QPushButton("Отмена", self)
            self.close_btn.resize(QSize(60, 40))
            self.close_btn.move(QPoint(280, 250))
            self.close_btn.clicked.connect(self.close)

        def add(self):
            accept_dlg = QMessageBox(self)
            accept_dlg.setWindowTitle("Подтверждение")
            accept_dlg.setText("Сохранить запись?")
            accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            but = accept_dlg.exec()

            if but == QMessageBox.Yes:
                self.close()

        def check_series(self):
            text = self.series_i.text()[:4]
            text = re.findall(r"[0-9]{4}", text)
            if text:
                self.series_i.setText(text[0])
                self.sender().setStyleSheet("border :1px solid ; border-color : green;")
                self.check1 = True
            else:
                self.series_i.setStyleSheet("border :1px solid ; border-color : red;")
                self.check1 = False

        def check_code_and_num(self):
            text = self.sender().text()[:6]
            text = re.findall(r"[0-9]{6}", text)
            if text:
                self.sender().setText(text[0])
                self.sender().setStyleSheet("border :1px solid ; border-color : green;")
                self.check2 = True
                if self.check2:
                    self.check3 = True
            else:
                self.sender().setStyleSheet("border :1px solid ; border-color : red;")
                self.check2 = False
                self.check3 = False

        def check_agency(self):
            text = "".join(re.findall(r"[а-яА-Я ]", self.agency_i.text()))
            if text:
                self.check4 = True
            else:
                self.check4 = False
            self.agency_i.setText(text)

        def check_all(self):
            if self.check1 and self.check2 and self.check3 and self.check4 and self.check5:
                self.ok_btn.setVisible(True)
            else:
                self.ok_btn.setVisible(False)

        def check_date(self):
            if self.birthday is not None and self.birthday != self.birth_i.date():
                self.update_date_windows(False, "red")
            elif self.birth_i.date().year() > self.issue_i.date().year() \
                    or self.issue_i.date().year() - self.birth_i.date().year() != 14:
                self.update_date_windows(False, "red")
            elif datetime.datetime.now().year - 18 > self.birth_i.date().year():
                self.update_date_windows(False, "red")
            else:
                self.update_date_windows(True, "green")

        def update_date_windows(self, is_ok, color):
            self.check5 = is_ok
            self.birth_i.setStyleSheet(f"border :1px solid ; border-color : {color};")
            self.issue_i.setStyleSheet(f"border :1px solid ; border-color : {color};")

    class InsertBirthCertificate(QDialog):
        def __init__(self, birthday):
            super().__init__()

            self.birthday = birthday
            self.check1 = self.check2 = self.check3 = False

            self.place_l = QLabel("Место рождения:", self)
            self.place_l.move(QPoint(30, 30))
            self.place_i = QLineEdit(self)
            self.place_i.resize(QSize(250, 20))
            self.place_i.move(QPoint(190, 30))
            self.place_i.textChanged.connect(self.check_place)
            self.place_i.textChanged.connect(self.check_all)

            self.agency_l = QLabel("Структурное подразделение:", self)
            self.agency_l.move(QPoint(30, 50))
            self.agency_i = QLineEdit(self)
            self.agency_i.resize(QSize(250, 20))
            self.agency_i.move(QPoint(190, 50))
            self.agency_i.textChanged.connect(self.check_agency)
            self.agency_i.textChanged.connect(self.check_all)

            self.birth_l = QLabel("Дата рождения:", self)
            self.birth_l.move(QPoint(30, 110))
            self.birth_i = QDateEdit(self)
            self.birth_i.move(QPoint(120, 110))
            self.birth_i.dateChanged.connect(self.check_date)
            self.birth_i.dateChanged.connect(self.check_all)

            self.issue_l = QLabel("Дата выдачи:", self)
            self.issue_l.move(QPoint(210, 110))
            self.issue_i = QDateEdit(self)
            self.issue_i.move(QPoint(290, 110))
            self.issue_i.dateChanged.connect(self.check_date)
            self.issue_i.dateChanged.connect(self.check_all)

            self.ok_btn = QPushButton("OK", self)
            self.ok_btn.resize(QSize(60, 40))
            self.ok_btn.move(QPoint(200, 250))
            self.ok_btn.setVisible(False)
            self.ok_btn.clicked.connect(self.add)

            self.close_btn = QPushButton("Отмена", self)
            self.close_btn.resize(QSize(60, 40))
            self.close_btn.move(QPoint(280, 250))
            self.close_btn.clicked.connect(self.close)

        def add(self):
            accept_dlg = QMessageBox(self)
            accept_dlg.setWindowTitle("Подтверждение")
            accept_dlg.setText("Сохранить запись?")
            accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            but = accept_dlg.exec()

            if but == QMessageBox.Yes:
                self.close()

        def check_all(self):
            if self.check1 and self.check2 and self.check3:
                self.ok_btn.setVisible(True)
            else:
                self.ok_btn.setVisible(False)

        def check_place(self):
            text = "".join(re.findall(r"[а-яА-Я ]", self.place_i.text()))
            if text:
                self.check1 = True
            else:
                self.check1 = False
            self.place_i.setText(text)

        def check_agency(self):
            text = "".join(re.findall(r"[а-яА-Я ]", self.agency_i.text()))
            if text:
                self.check2 = True
            else:
                self.check2 = False
            self.agency_i.setText(text)

        def check_date(self):
            if self.birthday is not None and self.birthday != self.birth_i.date():
                self.update_date_windows(False, "red")
            elif not 0 <= self.birth_i.date().year() - self.issue_i.date().year() <= 1:
                self.update_date_windows(False, "red")
            elif datetime.datetime.now().year - 18 > self.birth_i.date().year():
                self.update_date_windows(False, "red")
            else:
                self.update_date_windows(True, "green")

        def update_date_windows(self, is_ok, color):
            self.check3 = is_ok
            self.birth_i.setStyleSheet(f"border :1px solid ; border-color : {color};")
            self.issue_i.setStyleSheet(f"border :1px solid ; border-color : {color};")


class InsertStudentWindow(InsertHumanWindow):
    def __init__(self, bd):
        super().__init__(bd)

        self.is_birth = False
        self.birthday = None

        self.birth_btn = QPushButton("Добавить свид. о рождении", self)
        self.birth_btn.move(QPoint(150, 80))
        self.birth_btn.setVisible(False)

        self.passport_btn.clicked.connect(self.open_passport_window)
        self.birth_btn.clicked.connect(self.open_birth_window)

        self.groups_box = QComboBox(self)
        self.groups_box.move(QPoint(30, 120))
        self.fill_box()

        self.add_group_btn = QPushButton("Добавить", self)
        self.add_group_btn.move((QPoint(120, 120)))
        self.add_group_btn.clicked.connect(self.add_group)

        self.del_group_btn = QPushButton("Удалить", self)
        self.del_group_btn.move(QPoint(200, 120))
        self.del_group_btn.clicked.connect(self.del_group)
        self.del_group_btn.setVisible(False)

        self.add_groups_table = QListWidget(self)
        self.add_groups_table.move(QPoint(120, 160))
        self.add_groups_table.itemClicked.connect(self.set_visible_remove_btn)

        self.name_i.textChanged.connect(self.set_visible_final_btn)
        self.surname_i.textChanged.connect(self.set_visible_final_btn)
        self.email_i.textChanged.connect(self.set_visible_final_btn)

    def set_visible_remove_btn(self):
        self.del_group_btn.setVisible(True)

    def set_visible_final_btn(self):
        if self.is_name and self.is_surname and self.is_email:
            self.ok_btn.setVisible(True)

    def insert(self):
        accept_dlg = QMessageBox(self)
        accept_dlg.setWindowTitle("Подтверждение")
        accept_dlg.setText("Сохранить запись?")
        accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        but = accept_dlg.exec()

        if but == QMessageBox.Yes:
            if self.is_passport:
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO studentpasport (series, number, division_code, date_of_issue,"
                            f" authorized_agency, date_of_birthday) VALUES ('{self.passport_dict['series']}',"
                            f" '{self.passport_dict['number']}', '{self.passport_dict['division_code']}',"
                             f" '{self.passport_dict['date_of_issue']}', '{self.passport_dict['authorized_agency']}',"
                             f" '{self.passport_dict['date_of_birthday']}')")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                cur = self.bd.cursor()
                cur.execute(f"SELECT id_passport FROM studentpasport WHERE series='{self.passport_dict['series']}'"
                            f" AND number='{self.passport_dict['number']}'")
                id_passport = cur.fetchall()[0][0]
                cur.close()
                self.bd.reconnect()
            if self.is_birth:
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO studentbirthcertificate (date_of_issue, registration_place,"
                            f" authorized_agency, date_of_birthday) VALUES ('{self.birth_dict['date_of_issue']}'"
                            f", '{self.birth_dict['registration_place']}', '{self.birth_dict['authorized_agency']}',"
                            f" '{self.birth_dict['date_of_birthday']}')")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                cur = self.bd.cursor()
                cur.execute(f"SELECT id_certificate FROM studentbirthcertificate "
                            f"WHERE date_of_issue='{self.birth_dict['date_of_issue']}' AND"
                         f" registration_place='{self.birth_dict['registration_place']}' AND"
                         f" authorized_agency='{self.birth_dict['authorized_agency']}' AND"
                         f" date_of_birthday='{self.birth_dict['date_of_birthday']}'")
                id_birth = cur.fetchall()[0][0]
                cur.close()
                self.bd.reconnect()
            if self.is_birth and self.is_passport:
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO studentdocuments (id_passport, id_certificate)"
                            f" VALUES ({id_passport}, {id_birth})")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                cur = self.bd.cursor()
                cur.execute(f"SELECT id_documents FROM studentdocuments WHERE id_passport={id_passport}")
                id_doc = cur.fetchall()[0][0]
                cur.close()
                self.bd.reconnect()
            elif self.is_passport:
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO studentdocuments (id_passport) VALUES ({id_passport})")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                cur = self.bd.cursor()
                cur.execute(f"SELECT id_documents FROM studentdocuments WHERE id_passport={id_passport}")
                id_doc = cur.fetchall()[0][0]
                cur.close()
                self.bd.reconnect()
            elif self.is_birth:
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO studentdocuments (id_certificate) VALUES ({id_birth})")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                cur = self.bd.cursor()
                cur.execute(f"SELECT id_documents FROM studentdocuments WHERE id_certificate={id_birth}")
                id_doc = cur.fetchall()[0][0]
                cur.close()
                self.bd.reconnect()
            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO student (name_student, surname_student, email_student, status)"
                        f" VALUES ('{self.name_i.text()}', '{self.surname_i.text()}', '{self.email_i.text()}', 1)")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()
            cur = self.bd.cursor()
            cur.execute(f"SELECT id_student FROM student"
                        f" WHERE name_student='{self.name_i.text()}' AND surname_student='{self.surname_i.text()}'"
                        f" AND email_student='{self.email_i.text()}'")
            id_student = cur.fetchall()[0][0]
            cur.close()
            self.bd.reconnect()
            if self.is_birth or self.is_passport:
                cur = self.bd.cursor()
                cur.execute(f"UPDATE student SET id_documents={id_doc}"
                            f" WHERE id_student={id_student}")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
            for i in range(self.add_groups_table.count()):
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO studentgroup (id_student, id_group)"
                            f" VALUES ({id_student}, {self.add_groups_table.item(i).text().split('-')[0]})")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
            ok_btn = QMessageBox(self)
            ok_btn.setText("Запись создана")
            ok_btn.setStandardButtons(QMessageBox.Ok)
            ok_btn.exec()
            self.close()

    def open_passport_window(self):
        self.window = self.InsertPassport(self.birthday)
        self.window.exec()
        temp = self.window
        if temp.check1 and temp.check2 and temp.check3 and temp.check4 and temp.check5:
            self.is_passport = True
            birth_date = f"{temp.birth_i.date().year()}-{temp.birth_i.date().month()}-{temp.birth_i.date().day()}"
            issue_date = f"{temp.issue_i.date().year()}-{temp.issue_i.date().month()}-{temp.issue_i.date().day()}"
            if self.birthday is None:
                self.birthday = temp.birth_i.date()
            self.passport_dict = {"series": temp.series_i.text(), "number": temp.num_i.text(),
                                  "division_code": temp.code_i.text(), "date_of_issue": birth_date,
                                  "authorized_agency": temp.agency_i.text(), "date_of_birthday": issue_date}
            self.passport_btn.setStyleSheet("border :1px solid ; border-color : green;")
            self.passport_btn.setEnabled(False)

    def open_birth_window(self):
        self.window = self.InsertBirthCertificate(self.birthday)
        self.window.exec()
        temp = self.window
        if temp.check1 and temp.check2 and temp.check3:
            if self.birthday is None:
                self.birthday = temp.birth_i.date()
            self.is_birth = True
            birth_date = f"{temp.birth_i.date().year()}-{temp.birth_i.date().month()}-{temp.birth_i.date().day()}"
            issue_date = f"{temp.issue_i.date().year()}-{temp.issue_i.date().month()}-{temp.issue_i.date().day()}"
            self.birth_dict = {"date_of_issue": issue_date, "registration_place": temp.place_i.text(),
                               "authorized_agency": temp.agency_i.text(), "date_of_birthday": birth_date}
            self.birth_btn.setStyleSheet("border :1px solid ; border-color : green;")
            self.birth_btn.setEnabled(False)

    def fill_box(self):
        cur = self.bd.cursor()
        cur.execute(STUDENTS_TO_GROUP_REQUEST)
        data = cur.fetchall()
        self.groups_box.addItems([f"{i[2]}-{i[3]}" for i in data if i[0] - i[1] > 0])
        cur.close()
        self.bd.reconnect()

    def add_group(self):
        group = self.groups_box.currentText()
        self.groups_box.removeItem(self.groups_box.currentIndex())
        self.add_groups_table.addItem(group)

    def del_group(self):
        group = self.add_groups_table.takeItem(self.add_groups_table.currentRow())
        self.groups_box.addItem(group.text())
        self.del_group_btn.setVisible(False)


class InsertTeacherWindow(InsertHumanWindow):
    def __init__(self, db):
        super().__init__(db)

    def insert(self):
        self.close()


class InsertCourseWindow(InsertWindow):
    def __init__(self, db):
        super().__init__(db)

    def insert(self):
        self.close()


class InsertGroupWindow(InsertWindow):
    def __init__(self, db):
        super().__init__(db)

    def insert(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = InsertStudentWindow()
    ex.show()
    sys.excepthook = except_hook
    app.exec()
