from gui.base_tab import BaseTab
import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import ORM


class DeleteTab(BaseTab):
    def create_tab(self):
        delete_frame = ttk.Frame(self.notebook)
        self.notebook.add(delete_frame, text="Удаление записей")

        ttk.Label(delete_frame, text="Таблица:").grid(row=0, column=0, padx=5, pady=5)
        self.delete_table_var = tk.StringVar()
        (ttk.Combobox(delete_frame, textvariable=self.delete_table_var, values=["teachers", "subjects", "schedule"])
         .grid(row=0, column=1, padx=5, pady=5))

        ttk.Label(delete_frame, text="ID записи:").grid(row=1, column=0, padx=5, pady=5)
        self.delete_id_entry = ttk.Entry(delete_frame)
        self.delete_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(delete_frame, text="Удалить", command=self.delete_record).grid(row=2, column=0, columnspan=2,
                                                                                  pady=10)

    def delete_record(self):
        table_name = self.delete_table_var.get()
        record_id = self.delete_id_entry.get()

        try:
            record_id = int(record_id)
        except ValueError:
            messagebox.showerror("Ошибка", "ID записи должен быть целым числом")
            return

        message = ORM.delete_record(table_name, record_id)
        messagebox.showinfo("Удаление записи", message)

    def get_tab_name(self):
        return "Удаление записей"
