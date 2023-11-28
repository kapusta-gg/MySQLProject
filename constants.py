from PyQt5.QtCore import QSize

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
RU_TABLE_DICT_PROCEDURE = {"Ученики": "call students_info()",
                           "Преподователи": "call teachers_info()",
                           "Курсы": "call courses_info()",
                           "Группы": "call groups_info()"}
ADMIN_PASSWORD = "admin"
