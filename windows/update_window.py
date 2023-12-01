from PyQt5.QtWidgets import QDialog


class UpdateWidget(QDialog):
    def __init__(self, id_col):
        super().__init__()
        self.id_col = id_col


class UpdateStudentWidget(UpdateWidget):
    def __init__(self, id_col):
        super().__init__(id_col)


class UpdateTeacherWidget(UpdateWidget):
    def __init__(self, id_col):
        super().__init__(id_col)


class UpdateCourseWidget(UpdateWidget):
    def __init__(self, id_col):
        super().__init__(id_col)


class UpdateGroupWidget(UpdateWidget):
    def __init__(self, id_col):
        super().__init__(id_col)