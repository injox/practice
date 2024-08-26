import tkinter as tk
from gui.main_gui import DatabaseGUI


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
