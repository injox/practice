from gui.base_tab import BaseTab, table_columns
import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import ORM


class SearchTab(BaseTab):
    def create_tab(self):
        search_frame = ttk.Frame(self.notebook)
        search_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(search_frame, text="Поиск записей")

        control_frame = ttk.Frame(search_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Таблица:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_table_var = tk.StringVar()
        ttk.Combobox(control_frame, textvariable=self.search_table_var,
                     values=["teachers", "subjects", "schedule"]).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(control_frame, text="Поиск элементов:").pack(side=tk.LEFT, padx=(5, 5))
        self.search_criteria_entry = ttk.Entry(control_frame, width=50)
        self.search_criteria_entry.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(control_frame, text="Поиск", command=self.search_database).pack(side=tk.LEFT)

        self.search_result_text = tk.Text(search_frame, height=15, width=70)
        self.search_result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(search_frame, orient="vertical", command=self.search_result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_result_text.config(yscrollcommand=scrollbar.set)

    def search_database(self):
        table_name = self.search_table_var.get()
        search_term = self.search_criteria_entry.get()

        try:
            columns = table_columns[table_name]

            results = ORM.search_database(table_name, search_term)
            self.search_result_text.delete(1.0, tk.END)

            self.search_result_text.insert(tk.END, " | ".join(columns) + "\n")
            self.search_result_text.insert(tk.END, "-" * (len(" | ".join(columns)) + 1) + "\n")

            if results:
                for result in results:
                    self.search_result_text.insert(tk.END, str(result) + "\n")
            else:
                self.search_result_text.insert(tk.END, "Результаты не найдены.")
        except KeyError:
            messagebox.showerror("Error", "Выбрана неверная таблица")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_tab_name(self):
        return "Поиск записей"
