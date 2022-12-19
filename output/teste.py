# This Python file uses the following encoding: utf-8
import tkinter as tk
import os
import sys
from tkinter import messagebox as mb

local_path = r"C:\Users\elias\Documents\GitHub\python-automatics-data-alterations-in-xml-file\teste.py"
current_path = os.path.abspath('teste.py')
if current_path != local_path:
    mb.showwarning('Erro', 'Não está sendo executado no local ideal')
    sys.exit()
else:
    window = tk.Tk()
    window.mainloop()