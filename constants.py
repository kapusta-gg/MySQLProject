from PyQt5.QtCore import QSize

MAIN_WINDOW_SIZE = QSize(1000, 1000)
TABLES_FOR_INFO = ["Ученики", "Преподователи", "Курсы", "Группы"]
RU_TABLE_DICT_PROCEDURE = {"Ученики": "call students_info()",
                           "Преподователи": "call teachers_info()",
                           "Курсы": "call courses_info()",
                           "Группы": "call groups_info()"}
