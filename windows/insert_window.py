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

        self.ok_btn = QPushButton("OK", self)
        self.ok_btn.resize(QSize(60, 40))
        self.ok_btn.move(QPoint(200, 450))
        self.ok_btn.setVisible(False)
        self.ok_btn.clicked.connect(self.insert)

        self.close_btn = QPushButton("Отмена", self)
        self.close_btn.resize(QSize(60, 40))
        self.close_btn.move(QPoint(280, 450))
        self.close_btn.clicked.connect(self.close)

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

    class InsertMedCard(QDialog):
        def __init__(self, medcards, birthday):
            super().__init__()

            self.birthday_year = birthday
            self.medcards = medcards

            self.is_date = self.is_num = False

            self.setFixedSize(QSize(300, 200))
            self.date_l = QLabel("Дата получения:", self)
            self.date_l.move(QPoint(30, 30))
            self.date_i = QDateEdit(self)
            self.date_i.move(QPoint(120, 28))
            self.date_i.dateChanged.connect(self.filter_medcard_date)
            self.date_i.dateChanged.connect(self.check_bools)

            self.num_l = QLabel("Номер мед. книжки:", self)
            self.num_l.move(QPoint(30, 60))
            self.num_i = QLineEdit(self)
            self.num_i.move(QPoint(140, 60))
            self.num_i.textChanged.connect(self.filter_medcard_num)
            self.num_i.textChanged.connect(self.check_bools)

            self.ok_btn = QPushButton("OK", self)
            self.ok_btn.move(QPoint(60, 160))
            self.ok_btn.setVisible(False)
            self.ok_btn.clicked.connect(self.check)

            self.close_btn = QPushButton("Отмена", self)
            self.close_btn.move(QPoint(160, 160))
            self.close_btn.clicked.connect(self.close_w)

        def filter_medcard_num(self):
            text = re.findall(r"[0-9]{7}", self.num_i.text())
            if text:
                self.num_i.setText(text[0])
                if text[0] in self.medcards:
                    self.num_i.setStyleSheet("border :1px solid ; border-color : red;")
                    self.is_num = False
                else:
                    self.num_i.setStyleSheet("border :1px solid ; border-color : green;")
                    self.is_num = True

        def filter_medcard_date(self):
            if self.date_i.date().year() - self.birthday_year < 18:
                self.date_i.setStyleSheet("border :1px solid ; border-color : red;")
                self.is_date = False
            else:
                self.date_i.setStyleSheet("border :1px solid ; border-color : green;")
                self.is_date = True

        def check_bools(self):
            if self.is_num and self.is_date:
                self.ok_btn.setVisible(True)

        def close_w(self):
            self.is_date = self.is_num = False
            self.close()

        def check(self):
            accept_dlg = QMessageBox(self)
            accept_dlg.setWindowTitle("Подтверждение")
            accept_dlg.setText("Сохранить запись?")
            accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            but = accept_dlg.exec()

            if but == QMessageBox.Yes:
                self.close()


class InsertStudentWindow(InsertHumanWindow):
    def __init__(self, bd):
        super().__init__(bd)

        cur = self.bd.cursor()
        cur.execute("SELECT series, number FROM studentpasport")
        self.passports = [i[0] + i[1] for i in cur.fetchall()]
        cur.close()
        self.bd.reconnect()

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

    def set_visible_btn(self):
        if self.name_i.text() and self.surname_i.text():
            is_visible = True
        else:
            is_visible = False
        self.passport_btn.setVisible(is_visible)
        self.birth_btn.setVisible(is_visible)

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
        self.window = self.InsertPassport(self.birthday, self.passports)
        self.window.exec()
        temp = self.window
        if temp.check1 and temp.check2 and temp.check3 and temp.check4 and temp.check5:
            self.is_passport = True
            birth_date = f"{temp.birth_i.date().year()}-{temp.birth_i.date().month()}-{temp.birth_i.date().day()}"
            issue_date = f"{temp.issue_i.date().year()}-{temp.issue_i.date().month()}-{temp.issue_i.date().day()}"
            if self.birthday is None:
                self.birthday = temp.birth_i.date()
            self.passport_dict = {"series": temp.series_i.text(), "number": temp.num_i.text(),
                                  "division_code": temp.code_i.text(), "date_of_birthday": birth_date,
                                  "authorized_agency": temp.agency_i.text(), "date_of_issue": issue_date}
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

    class InsertPassport(QDialog):
        def __init__(self, birthday, passports):
            self.birthday = birthday
            self.passports = passports
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
                if self.sender() == self.num_i:
                    self.check2 = True
                else:
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
            if self.series_i.text() + self.num_i.text() in self.passports:
                self.check1 = self.check2 = False
                self.series_i.setStyleSheet("border :1px solid ; border-color : red;")
                self.num_i.setStyleSheet("border :1px solid ; border-color : red;")
            elif self.series_i.text() and self.num_i.text():
                self.check1 = self.check2 = True
                self.series_i.setStyleSheet("border :1px solid ; border-color : green;")
                self.num_i.setStyleSheet("border :1px solid ; border-color : green;")

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


class InsertTeacherWindow(InsertHumanWindow):
    def __init__(self, db):
        super().__init__(db)

        cur = self.bd.cursor()
        cur.execute("SELECT series, number FROM teacherpassport")
        self.passports = [i[0] + i[1] for i in cur.fetchall()]
        cur.close()
        self.bd.reconnect()

        cur = self.bd.cursor()
        cur.execute("SELECT number FROM teachermedcard")
        self.medcards = [i[0] for i in cur.fetchall()]
        cur.close()
        self.bd.reconnect()

        self.is_telephone = self.is_medcard = False

        self.telephone_l = QLabel("Телефон:", self)
        self.telephone_l.move(QPoint(180, 50))
        self.telephone_i = QLineEdit(self)
        self.telephone_i.resize(QSize(100, 20))
        self.telephone_i.move(QPoint(240, 50))
        self.telephone_i.textChanged.connect(self.filter_for_telephone)

        self.medcard_btn = QPushButton("Добавить мед. книжку", self)
        self.medcard_btn.move(QPoint(150, 120))
        self.passport_btn.move(QPoint(30, 120))
        self.medcard_btn.setVisible(False)

        self.edc_level_l = QLabel("Уровень образования:", self)
        self.edc_level_l.move(QPoint(30, 90))
        self.edc_level_box = QComboBox(self)
        self.edc_level_box.move(QPoint(150, 88))
        self.fill_edc_level_box()

        self.name_i.textChanged.connect(self.check_all)
        self.surname_i.textChanged.connect(self.check_all)
        self.email_i.textChanged.connect(self.check_all)
        self.telephone_i.textChanged.connect(self.check_all)

        self.passport_btn.clicked.connect(self.open_passport_window)
        self.medcard_btn.clicked.connect(self.open_medcard_window)

    def fill_edc_level_box(self):
        cur = self.bd.cursor()
        cur.execute("SELECT education_level FROM educationlevel")
        edc_lvl_data = cur.fetchall()
        cur.close()
        self.bd.reconnect()
        self.edc_level_box.addItems([i[0] for i in edc_lvl_data])

    def check_all(self):
        if self.is_name and self.is_surname and self.is_telephone and self.is_email and self.is_passport:
            self.ok_btn.setVisible(True)

    def filter_for_telephone(self):
        text = self.telephone_i.text()
        if text.startswith("+7"):
            text = text.replace("+7", "8")
        self.telephone_i.setText(text)
        text = re.findall(r"[8]{1}[0-9]{10}", text)
        if text:
            self.telephone_i.setText(text[0])
            self.telephone_i.setStyleSheet("border :1px solid ; border-color : green;")
            self.is_telephone = True
        else:
            self.telephone_i.setStyleSheet("border :1px solid ; border-color : red;")
            self.is_telephone = False

    def set_visible_btn(self):
        if self.name_i.text() and self.surname_i.text():
            is_visible = True
        else:
            is_visible = False
        self.passport_btn.setVisible(is_visible)

    def open_passport_window(self):
        self.window = self.InsertPassport(self.passports)
        self.window.exec()
        temp = self.window
        if temp.check1 and temp.check2 and temp.check3 and temp.check4 and temp.check5:
            self.is_passport = True
            birth_date = f"{temp.birth_i.date().year()}-{temp.birth_i.date().month()}-{temp.birth_i.date().day()}"
            issue_date = f"{temp.issue_i.date().year()}-{temp.issue_i.date().month()}-{temp.issue_i.date().day()}"
            self.passport_dict = {"series": temp.series_i.text(), "number": temp.num_i.text(),
                                  "division_code": temp.code_i.text(), "date_of_birthday": birth_date,
                                  "authorized_agency": temp.agency_i.text(), "date_of_issue": issue_date}
            self.passport_btn.setStyleSheet("border :1px solid ; border-color : green;")
            self.passport_btn.setEnabled(False)
            self.medcard_btn.setVisible(True)
            self.check_all()

    def open_medcard_window(self):
        self.window = self.InsertMedCard(self.medcards, int(self.passport_dict["date_of_birthday"].split("-")[0]))
        self.window.exec()
        temp = self.window
        if temp.is_num and temp.is_date:
            date = f"{temp.date_i.date().year()}-{temp.date_i.date().month()}-{temp.date_i.date().day()}"
            self.medcard_dict = {"date_of_issue": date, "number": temp.num_i.text()}
            self.is_medcard = True
            self.medcard_btn.setStyleSheet("border :1px solid ; border-color : green;")
            self.medcard_btn.setEnabled(False)

    class InsertPassport(QDialog):
        def __init__(self, passports):
            self.passports = passports
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
                if self.sender() == self.num_i:
                    self.check2 = True
                else:
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
            if self.series_i.text() + self.num_i.text() in self.passports:
                self.check1 = self.check2 = False
                self.series_i.setStyleSheet("border :1px solid ; border-color : red;")
                self.num_i.setStyleSheet("border :1px solid ; border-color : red;")
            elif self.series_i.text() and self.num_i.text():
                self.check1 = self.check2 = True
                self.series_i.setStyleSheet("border :1px solid ; border-color : green;")
                self.num_i.setStyleSheet("border :1px solid ; border-color : green;")

            if self.check1 and self.check2 and self.check3 and self.check4 and self.check5:
                self.ok_btn.setVisible(True)
            else:
                self.ok_btn.setVisible(False)

        def check_date(self):
            self.update_date_windows(True, "green")

        def update_date_windows(self, is_ok, color):
            self.check5 = is_ok
            self.birth_i.setStyleSheet(f"border :1px solid ; border-color : {color};")
            self.issue_i.setStyleSheet(f"border :1px solid ; border-color : {color};")

    def insert(self):
        accept_dlg = QMessageBox(self)
        accept_dlg.setWindowTitle("Подтверждение")
        accept_dlg.setText("Сохранить запись?")
        accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        but = accept_dlg.exec()

        if but == QMessageBox.Yes:
            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO teacherpassport (series, number, division_code, date_of_issue,"
                        f" authorized_agency, date_of_birthday) VALUES ('{self.passport_dict['series']}',"
                        f" '{self.passport_dict['number']}', '{self.passport_dict['division_code']}',"
                        f" '{self.passport_dict['date_of_issue']}', '{self.passport_dict['authorized_agency']}',"
                        f" '{self.passport_dict['date_of_birthday']}')")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"SELECT id_passport FROM teacherpassport "
                        f"WHERE series='{self.passport_dict['series']}' AND number='{self.passport_dict['number']}'")
            id_passport = cur.fetchall()[0][0]
            cur.close()
            self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO teacherdocuments (id_passport) VALUES ({id_passport})")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"SELECT id_documnets FROM teacherdocuments WHERE id_passport={id_passport}")
            id_doc = cur.fetchall()[0][0]
            cur.close()
            self.bd.reconnect()

            if self.is_medcard:
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO teachermedcard (date_of_issue, number)"
                            f" VALUES ('{self.medcard_dict['date_of_issue']}', '{self.medcard_dict['number']}')")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()

                cur = self.bd.cursor()
                cur.execute(f"SELECT id_medcard FROM teachermedcard WHERE number='{self.medcard_dict['number']}'")
                id_medcard = cur.fetchall()[0][0]
                cur.close()
                self.bd.reconnect()

                cur = self.bd.cursor()
                cur.execute(f"UPDATE teacherdocuments SET id_medcard={id_medcard} WHERE id_documnets={id_doc}")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO teacher (name_teacher, surname_teacher, telephone_number,"
                        f" work_email, education_level, id_documnets) VALUES ('{self.name_i.text()}',"
                        f" '{self.surname_i.text()}', '{self.telephone_i.text()}', '{self.email_i.text()}',"
                        f" {self.edc_level_box.currentIndex() + 1}, {id_doc})")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()

            ok_window = QMessageBox(self)
            ok_window.setText("Запись успешно создана")
            ok_window.setStandardButtons(QMessageBox.Ok)
            self.close()


class InsertCourseWindow(InsertWindow):
    def __init__(self, db):
        super().__init__(db)

    def insert(self):
        self.close()


class InsertGroupWindow(InsertWindow):
    def __init__(self, db):
        super().__init__(db)

        self.courses_l = QLabel("Курс:", self)
        self.courses_l.move(QPoint(30, 30))
        self.courses_box = QComboBox(self)
        self.courses_box.move(QPoint(60, 28))
        self.fill_courses_box()

        self.teachers_l = QLabel("Преподователь:", self)
        self.teachers_l.move(QPoint(200, 30))
        self.teachers_box = QComboBox(self)
        self.teachers_box.move(QPoint(290, 28))
        self.fill_teachers_box()

        self.days_l = QLabel("Дни недели:", self)
        self.days_l.move(QPoint(30, 60))
        self.deff = QLabel("---", self)
        self.deff.move(QPoint(200, 60))
        self.day_one = QComboBox(self)
        self.day_one.move(QPoint(100, 58))
        self.day_one.addItems(WEEK_DAYS[:-2])
        self.day_one.currentIndexChanged.connect(self.fill_second_day)
        self.day_one.currentIndexChanged.connect(self.check_schedule)
        self.day_two = QComboBox(self)
        self.day_two.move(QPoint(220, 58))
        self.fill_second_day()
        self.day_two.currentIndexChanged.connect(self.check_schedule)

        self.time_l = QLabel("Время:", self)
        self.time_l.move(QPoint(30, 90))
        self.time_box = QComboBox(self)
        self.time_box.move(QPoint(70, 88))
        self.time_box.addItems([str(i) for i in range(8, 19)])
        self.time_box.currentIndexChanged.connect(self.check_schedule)

        self.cabinet_l = QLabel("Кабинет:", self)
        self.cabinet_l.move(QPoint(140, 90))
        self.cabinet_box = QComboBox(self)
        self.cabinet_box.move(QPoint(190, 88))
        self.cabinet_box.addItems([str(i) for i in range(100, 126)])
        self.cabinet_box.currentIndexChanged.connect(self.check_schedule)
        self.cabinet_box.resize(QSize(50, 18))

        self.spots_l = QLabel("Макс. кол-во студентов:", self)
        self.spots_l.move(QPoint(250, 90))
        self.spots_box = QComboBox(self)
        self.spots_box.move(QPoint(380, 88))
        self.spots_box.addItems([str(i) for i in range(5, 21)])
        self.spots_box.currentIndexChanged.connect(self.is_visible_add)

        self.check_schedule()

        self.students_l = QLabel("Студенты:", self)
        self.students_l.move(QPoint(30, 120))

        self.students_box = QComboBox(self)
        self.students_box.move(QPoint(90, 118))
        self.fill_students_box()

        self.add_student_btn = QPushButton("Добавить", self)
        self.add_student_btn.move((QPoint(300, 118)))
        self.add_student_btn.clicked.connect(self.add_student)
        self.add_student_btn.clicked.connect(self.is_visible_add)

        self.del_student_btn = QPushButton("Удалить", self)
        self.del_student_btn.move(QPoint(380, 118))
        self.del_student_btn.setVisible(False)

        self.students_table = QListWidget(self)
        self.students_table.move(QPoint(120, 160))
        self.students_table.itemClicked.connect(self.is_visible_del)

    def add_student(self):
        student = self.students_box.currentText()
        self.students_table.addItem(student)
        self.students_box.removeItem(self.students_box.currentIndex())

    def is_visible_del(self):
        if self.students_table.count() == 0:
            self.del_student_btn.setVisible(False)
        else:
            self.del_student_btn.setVisible(True)

    def is_visible_add(self):
        if self.students_table.count() == int(self.spots_box.currentText()):
            self.add_student_btn.setVisible(False)
        elif self.students_table.count() > int(self.spots_box.currentText()):
            self.students_table.clear()
            self.students_box.clear()
            self.fill_students_box()
            self.add_student_btn.setVisible(True)
        else:
            self.add_student_btn.setVisible(True)

    def fill_students_box(self):
        cur = self.bd.cursor()
        cur.execute("SELECT id_student, name_student, surname_student FROM student WHERE status=1")
        students = cur.fetchall()
        cur.close()
        self.bd.reconnect()
        self.students_box.addItems([str(i[0]) + ". " + i[1] + " " + i[2] for i in students])

    def fill_second_day(self):
        self.day_two.clear()
        ind = self.day_one.currentIndex()
        self.day_two.addItems(WEEK_DAYS[ind + 1:])

    def fill_courses_box(self):
        cur = self.bd.cursor()
        cur.execute("SELECT id_course, name FROM course")
        courses = cur.fetchall()
        cur.close()
        self.bd.reconnect()
        self.courses_box.addItems([str(i[0]) + ". " + i[1] for i in courses])

    def fill_teachers_box(self):
        cur = self.bd.cursor()
        cur.execute("SELECT id_teacher, name_teacher, surname_teacher FROM teacher")
        teachers = cur.fetchall()
        cur.close()
        self.bd.reconnect()
        self.teachers_box.addItems([str(i[0]) + ". " + i[1] + " " + i[2] for i in teachers])

    def check_schedule(self):
        cur = self.bd.cursor()
        cur.execute(f"SELECT id_date_lessons FROM lessonsday WHERE cabinet={self.cabinet_box.currentText()}"
                    f" AND date_lessons='{self.day_one.currentText()}-{self.day_two.currentText()}'"
                    f" AND time_lessons=TIME('{self.time_box.currentText()}:00:00')")
        if cur.fetchall():
            self.cabinet_box.setStyleSheet("border :1px solid ; border-color : red;")
            self.time_box.setStyleSheet("border :1px solid ; border-color : red;")
            self.day_one.setStyleSheet("border :1px solid ; border-color : red;")
            self.day_two.setStyleSheet("border :1px solid ; border-color : red;")
            self.ok_btn.setVisible(False)
        else:
            self.cabinet_box.setStyleSheet("border :1px solid ; border-color : green;")
            self.time_box.setStyleSheet("border :1px solid ; border-color : green;")
            self.day_one.setStyleSheet("border :1px solid ; border-color : green;")
            self.day_two.setStyleSheet("border :1px solid ; border-color : green;")
            self.ok_btn.setVisible(True)
        cur.close()
        self.bd.reconnect()

    def insert(self):
        accept_dlg = QMessageBox(self)
        accept_dlg.setWindowTitle("Подтверждение")
        accept_dlg.setText("Сохранить запись?")
        accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        but = accept_dlg.exec()

        if but == QMessageBox.Yes:
            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO lessonsday (cabinet, date_lessons, time_lessons)"
                        f" VALUES ({self.cabinet_box.currentText()},"
                        f" '{self.day_one.currentText()}-{self.day_two.currentText()}',"
                        f" TIME('{self.time_box.currentText()}:00:00'))")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"SELECT id_date_lessons FROM lessonsday WHERE cabinet={self.cabinet_box.currentText()}"
                        f" AND date_lessons='{self.day_one.currentText()}-{self.day_two.currentText()}'"
                        f" AND time_lessons=TIME('{self.time_box.currentText()}:00:00')")
            id_date = cur.fetchall()[0][0]
            cur.close()
            self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO studygroup (max_students_in_group, id_date_lessons)"
                        f" VALUES ({self.spots_box.currentText()}, {id_date})")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"SELECT id_group FROM studygroup WHERE id_date_lessons={id_date}")
            id_group = cur.fetchall()[0][0]
            cur.close()
            self.bd.reconnect()

            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO groupteacher (id_group, id_teacher, id_course)"
                        f" VALUES ({id_group}, {self.teachers_box.currentText().split('.')[0]},"
                        f" {self.courses_box.currentText().split('.')[0]})")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()

            for i in range(self.students_table.count()):
                id_student = self.students_table.item(i).text().split('.')[0]
                cur = self.bd.cursor()
                cur.execute(f"INSERT INTO studentgroup (id_group, id_student)"
                            f" VALUES ({id_group}, {id_student})")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
            ok_window = QMessageBox(self)
            ok_window.setText("Запись успешно создана")
            ok_window.setStandardButtons(QMessageBox.Ok)
            self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    from database import create_connection
    app = QApplication(sys.argv)
    ex = InsertTeacherWindow(create_connection())
    ex.show()
    sys.excepthook = except_hook
    app.exec()
