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
    right_path = r"O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS"
    right_executable_name = "Alterador de Guias TISS.exe"
    current_executable_path = os.path.abspath(right_executable_name)
    current_executable_name = os.path.basename(__file__)
    print(f'{right_path}\\{right_executable_name}')
    print(current_executable_path)
    # if current_executable_name != "Alterador de Guias TISS.exe":
    #     close()
    #
    # elif current_local_path != f'{right_path}\\{right_executable_name}' :
    #     close()


closeApplicationIfConditionsNotAttend()
