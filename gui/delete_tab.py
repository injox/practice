from gui.base_tab import BaseTab
import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import ORM
from db.models import table_display_names


class DeleteTab(BaseTab):
    def create_tab(self):  # параметры вкладки
        delete_frame = ttk.Frame(self.notebook)
        self.notebook.add(delete_frame, text="Удаление записей")

        ttk.Label(delete_frame, text="Таблица:").grid(row=0, column=0, padx=5, pady=5)
        self.delete_table_var = tk.StringVar()
        (ttk.Combobox(delete_frame, textvariable=self.delete_table_var, values=list(table_display_names.values()))
         .grid(row=0, column=1, padx=5, pady=5))

        ttk.Label(delete_frame, text="ID записи:").grid(row=1, column=0, padx=5, pady=5)
        self.delete_id_entry = ttk.Entry(delete_frame)
        self.delete_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(delete_frame, text="Удалить", command=self.delete_record).grid(row=2, column=0, columnspan=2,
                                                                                  pady=10)

    def delete_record(self):  # удаление записи из бд
        table_display = self.delete_table_var.get()
        table_name = next(key for key, value in table_display_names.items() if value == table_display)
        record_id = self.delete_id_entry.get()

        try:
            record_id = int(record_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID записи должен быть целым числом")
            return

        message = ORM.delete_record(table_name, record_id)
        messagebox.showinfo("Удаление записи", message)

    def get_tab_name(self):  # название вкладки
        return "Удаление записей"
