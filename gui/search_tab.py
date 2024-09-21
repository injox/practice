from gui.base_tab import BaseTab, table_columns
import tkinter as tk
from tkinter import ttk, messagebox
from db.queries import ORM
from db.models import table_display_names, teacher_column_names, subject_column_names, schedule_column_names


column_mappings = {
    "teachers": teacher_column_names,
    "subjects": subject_column_names,
    "schedule": schedule_column_names
}


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
                     values=list(table_display_names.values())).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(control_frame, text="Поиск элементов:").pack(side=tk.LEFT, padx=(5, 5))
        self.search_criteria_entry = ttk.Entry(control_frame, width=50)
        self.search_criteria_entry.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(control_frame, text="Поиск", command=self.search_database).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(search_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(search_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def search_database(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        table_display = self.search_table_var.get()
        table_name = next(key for key, value in table_display_names.items() if value == table_display)
        search_term = self.search_criteria_entry.get()

        try:
            results = ORM.search_database(table_name, search_term)

            for i in self.tree.get_children():
                self.tree.delete(i)

            if isinstance(results, str):
                self.tree["columns"] = ["Message"]
                self.tree.heading("Message", text="Message")
                self.tree.insert("", "end", values=[results])
                return

            if not results:
                self.tree["columns"] = ["Message"]
                self.tree.heading("Message", text="Message")
                self.tree.insert("", "end", values=["Результаты не найдены."])
                return

            columns = list(results[0].keys())
            self.tree["columns"] = columns
            self.tree["show"] = "headings"

            for col in columns:
                display_name = column_mappings[table_name].get(col, col.capitalize())
                self.tree.heading(col, text=display_name)
                self.tree.column(col, anchor="center", width=100)

            for row in results:
                self.tree.insert("", "end", values=list(row.values()))

        except KeyError:
            messagebox.showerror("Error", "Выбрана неверная таблица")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_tab_name(self):
        return "Поиск записей"
