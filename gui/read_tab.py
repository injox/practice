from gui.base_tab import BaseTab
from tkinter import ttk, filedialog
import xml.etree.ElementTree as ET


class ReadTab(BaseTab):
    def create_tab(self):  # создание вкладки
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

    def select_xml_file(self):  # выбор файла
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.file_label.config(text=file_path)
            self.display_xml_content(file_path)

    def display_xml_content(self, file_path):  # отображение содержимого файла
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

    def get_tab_name(self):
        return "Чтение из XML"
