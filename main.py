# -*- coding: utf-8 -*-
"""
Главный файл приложения "Система управления студентами"
НКПиИТ - Новосибирский колледж печати и информационных технологий
"""

import tkinter as tk
from gui import CollegeApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CollegeApp(root)
    root.mainloop()