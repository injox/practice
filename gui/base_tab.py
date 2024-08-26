from abc import ABC, abstractmethod
from tkinter import ttk


class BaseTab(ABC):
    def __init__(self, notebook):
        self.notebook = notebook
        self.frame = ttk.Frame(self.notebook)
        self.create_tab()

    @abstractmethod
    def create_tab(self):
        pass

    @abstractmethod
    def get_tab_name(self):
        pass


table_columns = {
    "teachers": ["teacher_code", "name", "surname", "middle_name", "degree", "work_position", "experience"],
    "subjects": ["subject_code", "subject", "hours"],
    "schedule": ["teacher_code", "subject_code", "group_name"]
}
