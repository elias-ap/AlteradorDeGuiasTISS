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
    right_path = r"O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS\teste.exe"
    right_executable_name = "teste.exe"
    current_path = os.path.abspath(__file__)
    current_executable_name = os.path.basename(__file__)
    l = open('teste.txt', 'x')
    l.write(f'{right_path}\n{current_path}\n{current_executable_name}')
    if current_executable_name != right_executable_name:
        mb.showwarning('Erro', f'Nome diferente')
    elif current_path != right_path:
        mb.showwarning('Erro', f'Local diferente')
    else:
        window = tk.Tk()
        window.mainloop()

closeApplicationIfConditionsNotAttend()
