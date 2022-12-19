# This Python file uses the following encoding: utf-8
import tkinter as tk
import os
import sys
from tkinter import messagebox as mb

def close():
    mb.showwarning('Erro', f'A aplicação só executará no local:\n {right_path}')
    sys.exit()


def closeApplicationIfConditionsNotAttend():
    global right_path
    right_path = r"C:\Users\eliasp\Documents\GitHub\python-automatics-data-alterations-in-xml-file"
    right_executable_name = "teste.py"
    current_local_path = os.path.abspath(right_executable_name)
    current_executable_name = os.path.basename(__file__)
    if current_executable_name != "teste.py":
        close()

    elif current_local_path != f'{right_path}\\{right_executable_name}' :
        close()

closeApplicationIfConditionsNotAttend()
window = tk.Tk()
window.mainloop()