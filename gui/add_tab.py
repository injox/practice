from gui.base_tab import BaseTab, table_columns
import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import ORM
from db.models import schedule_column_names, subject_column_names, teacher_column_names, table_display_names

column_mappings = {
    "teachers": teacher_column_names,
    "subjects": subject_column_names,
    "schedule": schedule_column_names
}


class AddTab(BaseTab):
    def create_tab(self):  # задание параметров окна
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Добавить запись")

        ttk.Label(add_frame, text="Таблица:").grid(row=0, column=0, padx=5, pady=5)
        self.add_table_var = tk.StringVar()
        self.add_table_combobox = ttk.Combobox(add_frame, textvariable=self.add_table_var,
                                               values=list(table_display_names.values()))
        self.add_table_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.add_table_combobox.bind("<<ComboboxSelected>>", self.update_add_fields)

        self.add_fields_frame = ttk.Frame(add_frame)
        self.add_fields_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(add_frame, text="Добавить запись", command=self.add_record).grid(row=2, column=0, columnspan=2,
                                                                                    pady=10)

    def add_record(self):  # добавление данных в бд
        table_display = self.add_table_var.get()
        table_name = next(key for key, value in table_display_names.items() if value == table_display)
        mapping = column_mappings[table_name]
        data = {next((k for k, v in mapping.items() if v == column), column): entry.get()
                for column, entry in self.add_entries.items()}
        try:
            ORM.add_record(table_name, **data)
            messagebox.showinfo("Success", "Запись успешно добавлена.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_add_fields(self, event=None):  # обновление полей
        for widget in self.add_fields_frame.winfo_children():
            widget.destroy()

        table_display = self.add_table_var.get()
        table_name = next(key for key, value in table_display_names.items() if value == table_display)
        self.add_entries = {}

        mapping = column_mappings[table_name]
        for i, (_, column) in enumerate(mapping.items()):
            ttk.Label(self.add_fields_frame, text=f"{column}:").grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.add_fields_frame, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.add_entries[column] = entry

    def get_tab_name(self):  # название вкладки
        return "Добавить запись"
