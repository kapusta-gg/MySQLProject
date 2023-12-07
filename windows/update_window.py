from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QApplication, QPushButton, QComboBox, QListWidget,\
    QMessageBox, QCheckBox, QInputDialog, QErrorMessage, QDateEdit
from PyQt5.Qt import QSize, QPoint, QDate

from const.const_update_windows import *
from abc import abstractmethod

import re
import datetime

class UpdateWidget(QDialog):
    def __init__(self, id_row, bd):
        super().__init__()
        self.setFixedSize(WINDOW_SIZE)
        self.id_row = id_row
        self.bd = bd

        self.is_changed = False
        self.is_warned = False
        self.is_first_check = True
        self.is_admin = False

        self.check_admin = QCheckBox("Зайти как админ", self)
        self.check_admin.clicked.connect(self.give_admin_permission)

        self.data_dict = self.new_data_dict = None

        self.ok_btn = QPushButton("OK", self)
        self.ok_btn.resize(QSize(60, 40))
        self.ok_btn.move(QPoint(200, 450))
        self.ok_btn.setVisible(False)
        self.ok_btn.clicked.connect(self.update_col)

        self.close_btn = QPushButton("Выйти", self)
        self.close_btn.resize(QSize(60, 40))
        self.close_btn.move(QPoint(280, 450))
        self.close_btn.clicked.connect(self.close)

    def warn_user(self):
        warn_dlg = QMessageBox(self)
        warn_dlg.setText("Удаляя/Добавляя вы изменяете данные бд")
        warn_dlg.setStandardButtons(QMessageBox.Ok| QMessageBox.Cancel)
        btn = warn_dlg.exec()

        if btn == QMessageBox.Ok:
            self.is_warned = True

    def give_admin_permission(self):
        if self.check_admin.checkState():
            if self.is_first_check:
                text, ok = QInputDialog().getText(self, "Введите пароль", "Введите пароль администратора")
                if ok and text == ADMIN_PASSWORD:
                    self.is_admin = True
                    self.close_btn.setText("Отмена")
                else:
                    QErrorMessage(self).showMessage("Отказано в доступе")
                self.is_first_check = False
            else:
                self.is_admin = True
                self.close_btn.setText("Отмена")
        else:
            self.is_admin = False
            self.close_btn.setText("Выйти")

    @abstractmethod
    def update_col(self):
        pass


class UpdateHumanWidget(UpdateWidget):
    def __init__(self, id_row, bd):
        super().__init__(id_row, bd)

        self.is_name = self.is_surname = self.is_passport = False
        self.is_email = True
        self.groups_in = None

        self.name_l = QLabel("Имя:", self)
        self.name_l.move(QPoint(30, 30))
        self.name_i = QLineEdit(self)
        self.name_i.setEnabled(False)
        self.name_i.resize(QSize(100, 20))
        self.name_i.move(QPoint(70, 30))

        self.surname_l = QLabel("Фамилия:", self)
        self.surname_l.move(QPoint(180, 30))
        self.surname_i = QLineEdit(self)
        self.surname_i.setEnabled(False)
        self.surname_i.resize(QSize(100, 20))
        self.surname_i.move(QPoint(240, 30))

        self.email_l = QLabel("Почта:", self)
        self.email_l.move(QPoint(30, 50))
        self.email_i = QLineEdit(self)
        self.email_i.setEnabled(False)
        self.email_i.resize(QSize(100, 20))
        self.email_i.move(QPoint(70, 50))

        self.name_i.textChanged.connect(self.filter_for_names)
        self.surname_i.textChanged.connect(self.filter_for_names)
        self.email_i.textChanged.connect(self.filter_for_email)

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
        self.is_changed = True

    def filter_for_email(self):
        if not re.findall(r"[a-zA-Z0-9.]+[@]+[a-z]+[.]+[a-z]+", self.sender().text()):
            self.is_email = False
            self.sender().setStyleSheet("border :1px solid ; border-color : red;")
        else:
            self.is_email = True
            self.sender().setStyleSheet("border :1px solid ; border-color : green;")
        self.is_changed = True

    class CheckPassport(QDialog):
        def __init__(self, passport_data):
            super().__init__()
            self.setFixedSize(DOC_WINDOW_SIZE)
            self.series_l = QLabel("Серия:", self)
            self.series_l.move(QPoint(30, 30))
            self.series_i = QLineEdit(self)
            self.series_i.resize(QSize(100, 20))
            self.series_i.move(QPoint(70, 30))
            self.series_i.setEnabled(False)
            self.series_i.setText(passport_data["series"])

            self.num_l = QLabel("Номер:", self)
            self.num_l.move(QPoint(180, 30))
            self.num_i = QLineEdit(self)
            self.num_i.resize(QSize(100, 20))
            self.num_i.move(QPoint(220, 30))
            self.num_i.setEnabled(False)
            self.num_i.setText(passport_data["number"])

            self.code_l = QLabel("Код подразделения:", self)
            self.code_l.move(QPoint(30, 50))
            self.code_i = QLineEdit(self)
            self.code_i.resize(QSize(100, 20))
            self.code_i.move(QPoint(140, 50))
            self.code_i.setEnabled(False)
            self.code_i.setText(passport_data["division_code"])

            self.agency_l = QLabel("Структурное подразделение:", self)
            self.agency_l.move(QPoint(30, 80))
            self.agency_i = QLineEdit(self)
            self.agency_i.resize(QSize(250, 20))
            self.agency_i.move(QPoint(190, 80))
            self.agency_i.setEnabled(False)
            self.agency_i.setText(passport_data["authorized_agency"])

            self.birth_l = QLabel("Дата рождения:", self)
            self.birth_l.move(QPoint(30, 110))
            self.birth_i = QDateEdit(self)
            self.birth_i.move(QPoint(120, 110))
            self.birth_i.setEnabled(False)
            birth = passport_data["date_of_issue"]
            self.birth_i.setDate(QDate(birth.year, birth.month, birth.day))

            self.issue_l = QLabel("Дата выдачи:", self)
            self.issue_l.move(QPoint(210, 110))
            self.issue_i = QDateEdit(self)
            self.issue_i.move(QPoint(290, 110))
            self.issue_i.setEnabled(False)
            issue = passport_data["date_of_issue"]
            self.issue_i.setDate(QDate(issue.year, issue.month, issue.day))

            self.ok_btn = QPushButton("Выйти", self)
            self.ok_btn.resize(QSize(60, 40))
            self.ok_btn.move(QPoint(240, 250))
            self.ok_btn.clicked.connect(self.close)

    class CheckBirthCertificate(QDialog):
        def __init__(self, certificate_data):
            super().__init__()

            self.place_l = QLabel("Место рождения:", self)
            self.place_l.move(QPoint(30, 30))
            self.place_i = QLineEdit(self)
            self.place_i.resize(QSize(250, 20))
            self.place_i.move(QPoint(190, 30))
            self.place_i.setText(certificate_data["registration_place"])
            self.place_i.setEnabled(False)

            self.agency_l = QLabel("Структурное подразделение:", self)
            self.agency_l.move(QPoint(30, 50))
            self.agency_i = QLineEdit(self)
            self.agency_i.resize(QSize(250, 20))
            self.agency_i.move(QPoint(190, 50))
            self.agency_i.setText(certificate_data["authorized_agency"])
            self.agency_i.setEnabled(False)

            self.birth_l = QLabel("Дата рождения:", self)
            self.birth_l.move(QPoint(30, 110))
            self.birth_i = QDateEdit(self)
            self.birth_i.move(QPoint(120, 110))
            birth = certificate_data["date_of_birthday"]
            self.birth_i.setDate(QDate(birth.year, birth.month, birth.day))
            self.birth_i.setEnabled(False)

            self.issue_l = QLabel("Дата выдачи:", self)
            self.issue_l.move(QPoint(210, 110))
            self.issue_i = QDateEdit(self)
            self.issue_i.move(QPoint(290, 110))
            issue = certificate_data["date_of_issue"]
            self.issue_i.setDate(QDate(issue.year, issue.month, issue.day))
            self.issue_i.setEnabled(False)

            self.ok_btn = QPushButton("Выйти", self)
            self.ok_btn.resize(QSize(60, 40))
            self.ok_btn.move(QPoint(230, 250))
            self.ok_btn.clicked.connect(self.close)

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


class UpdateStudentWidget(UpdateHumanWidget):
    def __init__(self, id_row, bd):
        super().__init__(id_row, bd)
        cur = self.bd.cursor()
        cur.execute(f"call student_info({id_row}, 0)")
        table_names = [i[0] for i in cur.description]
        data = cur.fetchall()[0]
        self.data_dict = {table_names[i]: data[i] for i in range(len(data))}
        cur.close()
        self.bd.reconnect()
        cur = self.bd.cursor()
        cur.execute("SELECT series, number FROM studentpasport")
        self.passports = [i[0] + i[1] for i in cur.fetchall()]
        cur.close()
        self.bd.reconnect()

        self.is_birth = False

        self.birthday = None

        if self.data_dict["id_documents"] is not None:
            cur = self.bd.cursor()
            cur.execute(f"SELECT id_passport, id_certificate FROM studentdocuments"
                        f" WHERE id_documents={self.data_dict['id_documents']}")
            self.id_passport, self.id_certificate = cur.fetchall()[0]
            cur.close()
            self.bd.reconnect()
        else:
            self.id_passport = self.id_certificate = None

        self.check_admin.clicked.connect(self.check_permission)

        self.status_i = QLabel("Статус:", self)
        self.status_i.move(QPoint(180, 50))
        self.status_box = QComboBox(self)
        self.status_box.move(QPoint(240, 50))
        self.status_box.setEnabled(False)
        self.fill_status_box()

        self.groups_table = QListWidget(self)
        self.groups_table.move(QPoint(120, 160))
        self.groups_table.itemClicked.connect(self.set_visible_remove_btn)

        self.groups_box = QComboBox(self)
        self.groups_box.move(QPoint(30, 120))
        self.fill_groups_box()
        self.fill_groups_table()

        self.add_group_btn = QPushButton("Добавить", self)
        self.add_group_btn.move((QPoint(120, 120)))
        self.add_group_btn.clicked.connect(self.add_group)

        self.del_group_btn = QPushButton("Удалить", self)
        self.del_group_btn.move(QPoint(200, 120))
        self.del_group_btn.clicked.connect(self.del_group)
        self.del_group_btn.setVisible(False)

        self.passport_i = QLabel("Паспорт:", self)
        self.passport_i.move(QPoint(30, 90))
        self.add_passport_btn = QPushButton("Добавить", self)
        self.add_passport_btn.move(QPoint(80, 85))
        self.add_passport_btn.clicked.connect(self.add_passport)
        self.add_passport_btn.setVisible(False)
        self.check_passport_btn = QPushButton("Посмотреть", self)
        self.check_passport_btn.move(QPoint(80, 85))
        self.check_passport_btn.clicked.connect(self.check_passport)

        self.certificate_i = QLabel("Сертификат:", self)
        self.certificate_i.move(QPoint(160, 90))
        self.add_certificate_btn = QPushButton("Добавить", self)
        self.add_certificate_btn.move(QPoint(230, 85))
        self.add_certificate_btn.setVisible(False)
        self.add_certificate_btn.clicked.connect(self.add_certificate)
        self.check_certificate_btn = QPushButton("Посмотреть", self)
        self.check_certificate_btn.move(QPoint(230, 85))
        self.check_certificate_btn.clicked.connect(self.check_certificate)

        if self.id_passport is not None:
            cur = self.bd.cursor()
            cur.execute(f"SELECT date_of_birthday FROM studentpasport WHERE id_passport={self.id_passport}")
            self.birthday = cur.fetchall()[0][0]
            cur.close()
        if self.id_certificate is not None:
            cur = self.bd.cursor()
            cur.execute(f"SELECT date_of_birthday FROM studentbirthcertificate WHERE id_certificate={self.id_certificate}")
            self.birthday = cur.fetchall()[0][0]
            cur.close()
        self.set_old_data()
        self.name_i.textChanged.connect(self.update_name)
        self.surname_i.textChanged.connect(self.update_surname)
        self.email_i.textChanged.connect(self.update_email)
        self.status_box.currentTextChanged.connect(self.update_status)
        print(self.new_data_dict)

    def fill_groups_table(self):
        cur = self.bd.cursor()
        cur.execute(f"select distinct s.id_group, c.name from studentgroup s"
                    f" left join groupteacher g left join course c on g.id_course = c.id_course"
                    f" on g.id_group = s.id_group where s.id_student = {self.id_row}")
        data = [str(i[0]) + "-" + i[1] for i in cur.fetchall()]
        cur.close()
        self.bd.reconnect()
        self.groups_table.addItems(data)

    def fill_groups_box(self):
        cur = self.bd.cursor()
        cur.execute(f"select distinct s.max_students_in_group, curr_num_students(s.id_group), s.id_group, c.name"
                    f"  from studygroup s left join groupteacher g left join course c on c.id_course = g.id_course"
                    f" on g.id_group = s.id_group where s.id_group not in (select s2.id_group from studentgroup s2"
                    f" where s2.id_student = {self.id_row})")
        data = cur.fetchall()
        self.groups_box.addItems([f"{i[2]}-{i[3]}" for i in data if i[0] - i[1] > 0])
        cur.close()
        self.bd.reconnect()

    def fill_status_box(self):
        cur = self.bd.cursor()
        cur.execute(f"SELECT status FROM studentstatus")
        data = [i[0] for i in cur.fetchall()]
        cur.close()
        self.bd.reconnect()
        self.status_box.addItems(data)

    def set_visible_remove_btn(self):
        self.del_group_btn.setVisible(True)

    def set_old_data(self):
        self.name_i.setText(self.data_dict["name_student"])
        self.surname_i.setText(self.data_dict["surname_student"])
        self.email_i.setText(self.data_dict["email_student"])
        self.status_box.setCurrentIndex(self.data_dict["status"] - 1)
        self.new_data_dict = self.data_dict.copy()
        self.is_name = self.is_surname = self.is_changed = self.is_passport = self.is_certificate = False
        self.is_email = True
        self.add_passport_btn.setEnabled(True)
        self.add_passport_btn.setStyleSheet("border :1px solid ; border-color : gray;")
        self.add_certificate_btn.setEnabled(True)
        self.add_certificate_btn.setStyleSheet("border :1px solid ; border-color : gray;")

    def add_group(self):
        if not self.is_warned:
            self.warn_user()
        if self.is_warned:
            cur = self.bd.cursor()
            cur.execute(f"INSERT INTO studentgroup (id_student, id_group) VALUES"
                        f" ({self.id_row}, {self.groups_box.currentText().split('-')[0]})")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()
            group = self.groups_box.currentText()
            self.groups_box.removeItem(self.groups_box.currentIndex())
            self.groups_table.addItem(group)

    def add_passport(self):
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
            self.add_passport_btn.setStyleSheet("border :1px solid ; border-color : green;")
            self.add_passport_btn.setEnabled(False)
            self.ok_btn.setVisible(self.is_email)

    def add_certificate(self):
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
            self.add_certificate_btn.setStyleSheet("border :1px solid ; border-color : green;")
            self.add_certificate_btn.setEnabled(False)
            self.ok_btn.setVisible(self.is_email)

    def del_group(self):
        if not self.is_warned:
            self.warn_user()
        if self.is_warned:
            group = self.groups_table.takeItem(self.groups_table.currentRow())
            self.groups_box.addItem(group.text())
            self.del_group_btn.setVisible(False)
            cur = self.bd.cursor()
            cur.execute(f"DELETE FROM studentgroup WHERE id_student={self.id_row} AND id_group={group.text().split('-')[0]}")
            self.bd.commit()
            cur.close()
            self.bd.reconnect()

    def check_permission(self):
        if self.is_admin:
            self.name_i.setEnabled(True)
            self.surname_i.setEnabled(True)
            self.email_i.setEnabled(True)
            self.status_box.setEnabled(True)
            if self.id_passport is None and self.is_admin:
                self.add_passport_btn.setVisible(True)
                self.check_passport_btn.setVisible(False)
            else:
                self.check_passport_btn.setVisible(True)
            if self.id_certificate is None:
                self.add_certificate_btn.setVisible(True)
                self.check_certificate_btn.setVisible(False)
            else:
                self.check_certificate_btn.setVisible(True)
        else:
            self.name_i.setEnabled(False)
            self.surname_i.setEnabled(False)
            self.email_i.setEnabled(False)
            self.status_box.setEnabled(False)
            self.set_old_data()
            self.add_passport_btn.setVisible(False)
            self.check_passport_btn.setVisible(True)
            self.add_certificate_btn.setVisible(False)
            self.check_certificate_btn.setVisible(True)
        self.ok_btn.setVisible(False)

    def check_passport(self):
        if self.id_passport is None:
            dlg = QMessageBox(self)
            dlg.setText("У данной записи не существует паспорта")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec()
        else:
            cur = self.bd.cursor()
            cur.execute(f"SELECT date_of_birthday FROM studentpasport WHERE id_passport={self.id_passport}")
            table_names = [i[0] for i in cur.description]
            data = cur.fetchall()[0]
            cur.close()
            self.bd.reconnect()
            dlg = self.CheckPassport({table_names[i]:data[i] for i in range(len(data))})
            dlg.exec()

    def check_certificate(self):
        if self.id_certificate is None:
            dlg = QMessageBox(self)
            dlg.setText("У данной записи не существует паспорта")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.exec()
        else:
            cur = self.bd.cursor()
            cur.execute(f"SELECT * FROM studentbirthcertificate WHERE id_certificate={self.id_certificate}")
            table_names = [i[0] for i in cur.description]
            data = cur.fetchall()[0]
            cur.close()
            self.bd.reconnect()
            dlg = self.CheckBirthCertificate({table_names[i]:data[i] for i in range(len(data))})
            dlg.exec()

    def update_name(self):
        self.new_data_dict["name_student"] = self.name_i.text()
        self.ok_btn.setVisible(self.is_email)
        print(self.is_email)

    def update_surname(self):
        self.new_data_dict["surname_student"] = self.surname_i.text()
        self.ok_btn.setVisible(self.is_email)

    def update_email(self):
        self.new_data_dict["email_student"] = self.email_i.text()
        self.ok_btn.setVisible(self.is_email)

    def update_status(self):
        self.new_data_dict["status"] = self.status_box.currentIndex() - 1
        self.ok_btn.setVisible(self.is_email)

    def update_col(self):
        accept_dlg = QMessageBox(self)
        accept_dlg.setWindowTitle("Подтверждение")
        accept_dlg.setText("Сохранить обновление?")
        accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        but = accept_dlg.exec()

        if but == QMessageBox.Yes:
            for col, data in self.new_data_dict.items():
                cur = self.bd.cursor()
                if col == "status":
                    cur.execute(f"UPDATE student SET {col}={data} WHERE id_student={self.id_row}")
                elif col != "status" and col != "id_documents":
                    cur.execute(f"UPDATE student SET {col}='{data}' WHERE id_student={self.id_row}")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
            has_not_doc_id = False
            if self.new_data_dict["id_documents"] is None:
                has_not_doc_id = True
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
                if has_not_doc_id:
                    cur.execute(f"INSERT INTO studentdocuments (id_passport, id_certificate)"
                                f" VALUES ({id_passport}, {id_birth})")
                else:
                    cur.execute(f"UPDATE studentdocuments SET id_passport={id_passport}"
                                f" WHERE id_documents={self.new_data_dict['id_documents']}")
                    self.bd.commit()
                    cur.close()
                    self.bd.reconnect()
                    cur = self.bd.cursor()
                    cur.execute(f"UPDATE studentdocuments SET id_certificate={id_passport}"
                                f" WHERE id_documents={self.new_data_dict['id_documents']}")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                if has_not_doc_id:
                    id_doc = self.return_id_doc(id_passport, id_birth)
            elif self.is_passport:
                cur = self.bd.cursor()
                if has_not_doc_id:
                    cur.execute(f"INSERT INTO studentdocuments (id_passport) VALUES ({id_passport})")
                else:
                    cur.execute(f"UPDATE studentdocuments SET id_passport={id_passport}"
                                f" WHERE id_documents={self.new_data_dict['id_documents']}")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                if has_not_doc_id:
                    id_doc = self.return_id_doc(id_passport, None)
            elif self.is_birth:
                cur = self.bd.cursor()
                if has_not_doc_id:
                    cur.execute(f"INSERT INTO studentdocuments (id_certificate) VALUES ({id_birth})")
                else:
                    cur.execute(f"UPDATE studentdocuments SET id_certificate={id_birth}"
                                f" WHERE id_documents={self.new_data_dict['id_documents']}")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
                if has_not_doc_id:
                    id_doc = self.return_id_doc(None, id_birth)
            if has_not_doc_id:
                cur = self.bd.cursor()
                cur.execute(f"UPDATE student SET id_documents={id_doc} WHERE id_student={self.id_row}")
                self.bd.commit()
                cur.close()
                self.bd.reconnect()
            ok_window = QMessageBox(self)
            ok_window.setText("Запись успешно обновлена")
            ok_window.setStandardButtons(QMessageBox.Ok)
            ok_window.exec()
            self.close()

    def return_id_doc(self, id_p, id_c):
        cur = self.bd.cursor()
        if id_p is not None:
            cur.execute(f"SELECT id_documents FROM studentdocuments WHERE id_passport={id_p}")
        else:
            cur.execute(f"SELECT id_documents FROM studentdocuments WHERE id_certificate={id_c}")
        id_doc = cur.fetchall()[0][0]
        cur.close()
        self.bd.reconnect()
        return id_doc

    class InsertPassport(QDialog):
        def __init__(self, birthday, passports):
            super().__init__()
            self.birthday = birthday
            self.passports = passports
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


class UpdateTeacherWidget(UpdateWidget):
    def __init__(self, id_row):
        super().__init__(id_row)

    def update_col(self):
        accept_dlg = QMessageBox(self)
        accept_dlg.setWindowTitle("Подтверждение")
        accept_dlg.setText("Сохранить запись?")
        accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        but = accept_dlg.exec()

        if but == QMessageBox.Yes:
            ok_window = QMessageBox(self)
            ok_window.setText("Запись успешно создана")
            ok_window.setStandardButtons(QMessageBox.Ok)
            ok_window.exec()
            self.close()


class UpdateCourseWidget(UpdateWidget):
    def __init__(self, id_row):
        super().__init__(id_row)

    def update_col(self):
        pass


class UpdateGroupWidget(UpdateWidget):
    def __init__(self, id_row):
        super().__init__(id_row)

    def update_col(self):
        accept_dlg = QMessageBox(self)
        accept_dlg.setWindowTitle("Подтверждение")
        accept_dlg.setText("Сохранить запись?")
        accept_dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        but = accept_dlg.exec()

        if but == QMessageBox.Yes:
            ok_window = QMessageBox(self)
            ok_window.setText("Запись успешно создана")
            ok_window.setStandardButtons(QMessageBox.Ok)
            ok_window.exec()
            self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    from database import create_connection
    import sys
    app = QApplication(sys.argv)
    ex = UpdateStudentWidget("8", create_connection())
    ex.show()
    sys.excepthook = except_hook
    app.exec()