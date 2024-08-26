from gui.add_tab import AddTab
from gui.display_tab import DisplayTab
from gui.search_tab import SearchTab
from gui.update_tab import UpdateTab
from gui.delete_tab import DeleteTab
from gui.export_tab import ExportTab
from gui.read_tab import ReadTab
import tkinter as tk
from tkinter import ttk


class DatabaseGUI:  # основной класс интерфейса, отвечающий за создание вкладок
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Database Management System")
        self.master.geometry("800x600")

        self.notebook = ttk.Notebook(self.master, height=800, width=600)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.add_tab = AddTab(self.notebook)
        self.display_tab = DisplayTab(self.notebook)
        self.search_tab = SearchTab(self.notebook)
        self.update_tab = UpdateTab(self.notebook)
        self.delete_tab = DeleteTab(self.notebook)
        self.export_tab = ExportTab(self.notebook)
        self.read_tab = ReadTab(self.notebook)
