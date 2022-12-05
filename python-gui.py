import tkinter as ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

def createSaveButton():
    save_button = ttk.Button(window, text='Salvar a guia', command='af', anchor='se')
    save_button.pack(side='right', expand=True)

def escolheArquivo():
    tipoArquivo = (('XML files', '*.xml'), ( 'All files', '*.*'))
    global guia
    guia = fd.askopenfilename(filetypes=tipoArquivo)
    if guia != '':
        # cancel_button = ttk.Button(window, text='Cancelar')
        # cancel_button.grid(padx=10,pady=10)
        # cancel_button.pack(side='bottom')
        load_button['state'] = 'disabled'
        createSaveButton()
    else:
        mb.showwarning(title='Erro' ,message='A guia não foi escolhida!')

window = ttk.Tk()
window.title('Alterador de guias TISS')
window.geometry('400x250')
window.eval('tk::PlaceWindow . center')

load_button = ttk.Button(window, text='Escolher a guia', command=lambda:escolheArquivo(), anchor='sw')
load_button.grid_configure(pady=200, padx=30)

window.mainloop()
print(guia)