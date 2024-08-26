from gui.base_tab import BaseTab
import tkinter as tk
from tkinter import ttk
from db.queries import ORM


class DisplayTab(BaseTab):
    def create_tab(self):
        display_frame = ttk.Frame(self.notebook)
        display_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(display_frame, text="Отобразить данные")

        control_frame = ttk.Frame(display_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Таблица:").pack(side=tk.LEFT, padx=(0, 5))
        self.display_table_var = tk.StringVar()
        ttk.Combobox(control_frame, textvariable=self.display_table_var,
                     values=["teachers", "subjects", "schedule"]).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(control_frame, text="Отобразить данные", command=self.display_data).pack(side=tk.LEFT)

        self.display_text = tk.Text(display_frame, height=15, width=70)
        self.display_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.display_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def display_data(self):
        table_name = self.display_table_var.get()
        self.display_text.delete(1.0, tk.END)
        data = ORM.display_data(table_name)
        self.display_text.insert(tk.END, data)

    def get_tab_name(self):
        return "Отобразить данные"
