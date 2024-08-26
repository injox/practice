from gui.base_tab import BaseTab
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db.queries import ORM


class ExportTab(BaseTab):
    def create_tab(self):
        export_frame = ttk.Frame(self.notebook)
        self.notebook.add(export_frame, text="Экпортировать в XML")

        ttk.Button(export_frame, text="Выбрать файл", command=self.select_output_directory).grid(row=0, column=0,
                                                                                                 pady=10)
        self.output_directory_label = ttk.Label(export_frame, text="Путь к файлу не выбран")
        self.output_directory_label.grid(row=0, column=1, pady=10)

        ttk.Label(export_frame, text="Выбрать таблицу:").grid(row=1, column=0, padx=5, pady=5)
        self.export_table_var = tk.StringVar()
        self.export_table_combobox = ttk.Combobox(export_frame, textvariable=self.export_table_var,
                                                  values=["teachers", "subjects", "schedule"])
        self.export_table_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(export_frame, text="Экпортировать в XML", command=self.export_to_xml).grid(row=2, column=0,
                                                                                              columnspan=2, pady=10)

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            self.output_directory_label.config(text=self.output_directory)

    def export_to_xml(self):
        if not hasattr(self, 'output_directory'):
            messagebox.showerror("Error", "Выберите путь к файлу")
            return
        selected_table = self.export_table_var.get()
        if not selected_table:
            messagebox.showerror("Error", "Выберите таблицу")
            return
        message = ORM.export_database_to_xml(self.output_directory, selected_table)
        messagebox.showinfo("Данные экспортированы", message)

    def get_tab_name(self):
        return "Экспорт в XML"
