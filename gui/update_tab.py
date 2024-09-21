from gui.base_tab import BaseTab, table_columns
import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import ORM
from db.models import schedule_column_names, subject_column_names, teacher_column_names, table_display_names


class UpdateTab(BaseTab):
    def create_tab(self):
        update_frame = ttk.Frame(self.notebook)
        self.notebook.add(update_frame, text="Обновление данных")

        ttk.Label(update_frame, text="Таблица:").grid(row=0, column=0, padx=5, pady=5)
        self.update_table_var = tk.StringVar()
        self.update_table_combobox = ttk.Combobox(update_frame, textvariable=self.update_table_var,
                                                  values=list(table_display_names.values()))
        self.update_table_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.update_table_combobox.bind("<<ComboboxSelected>>", self.update_update_fields)

        ttk.Label(update_frame, text="Столбец:").grid(row=1, column=0, padx=5, pady=5)
        self.update_column_var = tk.StringVar()
        self.update_column_combobox = ttk.Combobox(update_frame, textvariable=self.update_column_var)
        self.update_column_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(update_frame, text="ID ряда:").grid(row=2, column=0, padx=5, pady=5)
        self.update_row_id_entry = ttk.Entry(update_frame)
        self.update_row_id_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(update_frame, text="Новое значение:").grid(row=3, column=0, padx=5, pady=5)
        self.update_new_value_entry = ttk.Entry(update_frame)
        self.update_new_value_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(update_frame, text="Обновить", command=self.update_data).grid(row=4, column=0, columnspan=2, pady=10)

    def update_data(self):
        table_display = self.update_table_var.get()
        table_name = next(key for key, value in table_display_names.items() if value == table_display)
        column_display = self.update_column_var.get()
        column = next(key for key, value in self.column_names.items() if value == column_display)
        row_id = self.update_row_id_entry.get()
        new_value = self.update_new_value_entry.get()

        if not all([table_name, column, row_id, new_value]):
            messagebox.showerror("Error", "Заполните все поля")
            return

        try:
            row_id = int(row_id)
        except ValueError:
            messagebox.showerror("Error", "Номер ряда должен быть целым числом")
            return

        try:
            ORM.update_data(table_name, column, row_id, new_value)
            messagebox.showinfo("Success", "Данные успешно обновлены")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_update_fields(self, event=None):
        table_display = self.update_table_var.get()
        table_name = next(key for key, value in table_display_names.items() if value == table_display)
        if table_name == 'teachers':
            self.column_names = teacher_column_names
        elif table_name == 'subjects':
            self.column_names = subject_column_names
        elif table_name == 'schedule':
            self.column_names = schedule_column_names
        else:
            self.column_names = {}

        self.update_column_combobox['values'] = list(self.column_names.values())
        self.update_column_var.set('')

    def get_tab_name(self):
        return "Обновление данных"
