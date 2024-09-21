from gui.base_tab import BaseTab
import tkinter as tk
from tkinter import ttk
from db.queries import ORM
from db.models import schedule_column_names, subject_column_names, teacher_column_names, table_display_names


class DisplayTab(BaseTab):
    def create_tab(self):  # создание вкладки
        display_frame = ttk.Frame(self.notebook)
        display_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(display_frame, text="Отобразить данные")

        control_frame = ttk.Frame(display_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Таблица:").pack(side=tk.LEFT, padx=(0, 5))
        self.display_table_var = tk.StringVar()
        ttk.Combobox(control_frame, textvariable=self.display_table_var,
                     values=list(table_display_names.values())).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(control_frame, text="Отобразить данные", command=self.display_data).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(display_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def display_data(self):  # отображение данных
        table_display = self.display_table_var.get()
        table_name = next(key for key, value in table_display_names.items() if value == table_display)
        data = ORM.display_data(table_name)
        next(key for key, value in table_display_names.items() if value == table_display)
        for i in self.tree.get_children():
            self.tree.delete(i)

        if not data:
            self.tree["columns"] = ["Message"]
            self.tree.heading("Message", text="Message")
            self.tree.insert("", "end", values=["No data available"])
            return

        columns = list(data[0].keys())
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        if table_name == 'schedule':
            self.column_names = schedule_column_names
        elif table_name == 'subjects':
            self.column_names = subject_column_names
        elif table_name == 'teachers':
            self.column_names = teacher_column_names
        else:
            self.column_names = {}

        for col in columns:
            display_name = self.column_names.get(col, col.capitalize())
            self.tree.heading(col, text=display_name)
            self.tree.column(col, anchor="center", width=100)

        for row in data:
            self.tree.insert("", "end", values=list(row.values()))

    def get_tab_name(self):  # получение названия вкладки
        return "Отобразить данные"
