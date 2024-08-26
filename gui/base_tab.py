from abc import ABC, abstractmethod
from tkinter import ttk


class BaseTab(ABC): # абстрактный класс, от которого наследуются все остальные
    def __init__(self, notebook):
        self.notebook = notebook
        self.frame = ttk.Frame(self.notebook)
        self.create_tab()

    @abstractmethod
    def create_tab(self):  # создание вкладки
        pass

    @abstractmethod
    def get_tab_name(self): # получение названия вкладки
        pass


table_columns = {  # словарь с названиями таблиц и их колонок
    "teachers": ["teacher_code", "name", "surname", "middle_name", "degree", "work_position", "experience"],
    "subjects": ["subject_code", "subject", "hours"],
    "schedule": ["teacher_code", "subject_code", "group_name"]
}
