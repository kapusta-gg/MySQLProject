from PyQt5.QtCore import QSize
from windows.update_window import *

UPDATE_SECONDS = 5
SEC_IN_MILISEC = 1000
MAIN_WINDOW_SIZE = QSize(1000, 1000)
TABLES_FOR_INFO = ["Ученики", "Преподователи", "Курсы", "Группы"]
DATABASE_TABLES = {"Ученики": "student",
                   "Преподователи": "teacher",
                   "Курсы": "course",
                   "Группы": "studygroup"}
COL_ID_NAME_DATABASE_TABLES = {"Ученики": "id_student",
                               "Преподователи": "id_teacher",
                               "Курсы": "id_course",
                               "Группы": "id_group"}
ADMIN_PASSWORD = "admin"

UPDATE_WINDOWS_DICT = {"Ученики": UpdateStudentWidget,
                       "Преподователи": UpdateTeacherWidget,
                       "Курсы": UpdateCourseWidget,
                       "Группы": UpdateGroupWidget}
