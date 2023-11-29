RU_TABLE_DICT_PROCEDURE = {"Ученики": "call students_info()",
                           "Преподователи": "call teachers_info()",
                           "Курсы": "call courses_info()",
                           "Группы": "call groups_info()"}

FILTER_REQUEST = {"Ученики": "select s.id_student, s.name_student, s.surname_student, s.email_student, ss.status from "
                             "student s left join studentstatus ss on ss.id_status = s.status where",
                  "Преподователи": "select t.id_teacher, t.name_teacher, t.surname_teacher, t.telephone_number, "
                                   "t.work_email, e.education_level from teacher t left join educationlevel e on "
                                   "e.id_education_level = t.education_level where",
                  "Курсы": "select c.id_course, c.name,c.duration, c.complexity from course c where",
                  "Группы": "select sp.id_group, sp.max_students_in_group, l.cabinet, l.time_lessons, l.date_lessons "
                            "from studygroup sp left join lessonsday l on l.id_date_lessons = sp.id_date_lessons where"}
COL_NAME_REQUEST = {"Ученики": ["s.id_student", "s.name_student", "s.surname_student", "s.email_student", "ss.status"],
                    "Преподователи": ["t.id_teacher", "t.name_teacher", "t.surname_teacher",
                                      "t.telephone_number", "t.work_email", "e.education_level"],
                    "Курсы": ["c.id_course", "c.name", "c.duration", "c.complexity"],
                    "Группы": ["sp.id_group", "sp.max_student_in_group", "l.cabinet",
                               "l.time_lessons", "l.date_lessons"]}
