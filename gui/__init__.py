# Всё относящееся к GUI
# add_tab - добавление данных в бд
# base_tab - хранение абстрактного класса и словаря с названия таблиц и их колонок
# delete_tab - удаление данных из бд
# display_tab - отображение данных одной из таблиц бд
# export_tab - экспорт данных из бд в xml файл
# main_gui - главный класс, запускающий приложение
# read_tab - чтение данных из xml файла
# search_tab - поиск данных в бд
# update_tab - обновление данных в бд

def __init__(self, notebook):
    super().__init__(notebook)
    self.teacher_column_names = {
        "id": "ID",
        "teacher_code": "Код учителя",
        "name": "Имя",
        "surname": "Фамилия",
        "middle_name": "Отчество",
        "degree": "Учёная степень",
        "work_position": "Должность",
        "experience": "Опыт работы(в годах)"
    }
    self.subject_column_names = {
        "id": "ID",
        "subject_code": "Код предмета",
        "subject": "Название",
        "hours": "Количество часов"
    }
    self.schedule_column_names = {
        "id": "ID",
        "teacher_code": "Преподаватель",
        "subject_code": "Предмет",
        "group_name": "Группа"
    }

