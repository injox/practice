import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db.queries import ORM
import xml.etree.ElementTree as ET


table_columns = {
    "Преподаватели": ["teacher_code", "name", "surname", "middle_name", "degree", "work_position", "experience"],
    "Предметы": ["subject_code", "subject", "hours"],
    "Нагрузка": ["teacher_code", "subject_code", "group_name"]
}


class DatabaseGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Database Management System")
        self.master.geometry("800x600")

        self.notebook = ttk.Notebook(self.master, height=800, width=600)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_add_tab()
        self.create_display_tab()
        self.create_search_tab()  
        self.create_update_tab()
        self.create_delete_tab()
        self.create_export_tab()
        self.create_read_tab()

    def create_add_tab(self):
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Добавить запись")

        ttk.Label(add_frame, text="Таблица:").grid(row=0, column=0, padx=5, pady=5)
        self.add_table_var = tk.StringVar()
        self.add_table_combobox = ttk.Combobox(add_frame, textvariable=self.add_table_var,
                                               values=list(table_columns.keys()))
        self.add_table_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.add_table_combobox.bind("<<ComboboxSelected>>", self.update_add_fields)

        self.add_fields_frame = ttk.Frame(add_frame)
        self.add_fields_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(add_frame, text="Добавить запись", command=self.add_record).grid(row=2, column=0, columnspan=2,
                                                                                    pady=10)

    def update_add_fields(self):
        for widget in self.add_fields_frame.winfo_children():
            widget.destroy()

        table = self.add_table_var.get()
        self.add_entries = {}

        for i, column in enumerate(table_columns[table]):
            ttk.Label(self.add_fields_frame, text=f"{column}:").grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.add_fields_frame, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.add_entries[column] = entry

    def add_record(self):
        table_name = self.add_table_var.get()
        data = {column: entry.get() for column, entry in self.add_entries.items()}
        try:
            ORM.add_record(table_name, **data)
            messagebox.showinfo("Success", "Запись успешно добавлена.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_display_tab(self):
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

    def create_search_tab(self):
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Поиск записей")

        ttk.Label(search_frame, text="Таблица:").grid(row=0, column=0, padx=5, pady=5)
        self.search_table_var = tk.StringVar()
        ttk.Combobox(search_frame, textvariable=self.search_table_var,
                     values=["teachers", "subjects", "schedule"]).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Поиск элементов:").grid(row=1, column=0, padx=5, pady=5)
        self.search_criteria_entry = ttk.Entry(search_frame, width=50)
        self.search_criteria_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(search_frame, text="Поиск", command=self.search_database).grid(row=2, column=0, columnspan=2,
                                                                                  pady=10)

        self.search_result_text = tk.Text(search_frame, height=15, width=70)
        self.search_result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def create_update_tab(self):
        update_frame = ttk.Frame(self.notebook)
        self.notebook.add(update_frame, text="Обновление данных")

        ttk.Label(update_frame, text="Таблица:").grid(row=0, column=0, padx=5, pady=5)
        self.update_table_var = tk.StringVar()
        self.update_table_combobox = ttk.Combobox(update_frame, textvariable=self.update_table_var,
                                                  values=list(table_columns.keys()))
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

        ttk.Button(update_frame, text="Обновить", command=self.update_data).grid(row=4, column=0, columnspan=2,
                                                                                 pady=10)

    def create_delete_tab(self):
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

    def create_export_tab(self):
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

    def create_read_tab(self):
        read_frame = ttk.Frame(self.notebook)
        self.notebook.add(read_frame, text="Чтение из XML")

        read_frame.grid_columnconfigure(0, weight=1)
        read_frame.grid_rowconfigure(1, weight=1)

        ttk.Button(read_frame, text="Выберите XML файл", command=self.select_xml_file).grid(row=0, column=0, padx=5,
                                                                                            pady=5, sticky='w')
        self.file_label = ttk.Label(read_frame, text="Файл не выбран")
        self.file_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.tree = ttk.Treeview(read_frame)
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        scrollbar = ttk.Scrollbar(read_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def select_xml_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.file_label.config(text=file_path)
            self.display_xml_content(file_path)

    def display_xml_content(self, file_path):
        tree = ET.parse(file_path)
        tree_root = tree.getroot()

        for i in self.tree.get_children():
            self.tree.delete(i)

        columns = ['id', 'subject_code', 'subject', 'hours']
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center", width=120)

        for record in tree_root.findall('record'):
            values = [record.find(col).text for col in columns]
            self.tree.insert("", "end", values=values)

    def display_data(self):
        table_name = self.display_table_var.get()
        self.display_text.delete(1.0, tk.END)
        data = ORM.display_data(table_name)
        self.display_text.insert(tk.END, data)

    def search_database(self):
        table_name = self.search_table_var.get()
        search_term = self.search_criteria_entry.get()

        try:
            results = ORM.search_database(table_name, search_term)
            self.search_result_text.delete(1.0, tk.END)
            if results:
                for result in results:
                    self.search_result_text.insert(tk.END, str(result) + "\n")
            else:
                self.search_result_text.insert(tk.END, "Результаты не найдены.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_data(self):
        table_name = self.update_table_var.get()
        column = self.update_column_var.get()
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

    def update_update_fields(self):
        table = self.update_table_var.get()
        columns = table_columns[table]
        self.update_column_combobox['values'] = columns
        self.update_column_var.set('')

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


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
