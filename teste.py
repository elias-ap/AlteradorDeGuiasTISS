import xml.etree.ElementTree as ET
import tkinter as ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb


def createGui():
    # Create main Window
    window = ttk.Tk()
    window.title('Alterador de guias TISS')
    window.geometry('400x250')
    window.eval('tk::PlaceWindow . center')
    window.maxsize(width=400, height=250)

    #  Create button Frame
    button_frame = ttk.Frame(window)  # , background='blue')
    button_frame.pack(side='bottom', pady=12, padx=100)

    button_frame2 = ttk.Frame(window)  # , background='blue')
    button_frame2.place(y=100, x=290)

    #       Create buttons

    global cancel_button, chooseGuide_button, saveGuide_button, generateHashAndSave_button, \
        doAlteration_button, data_alteration_check_button, value_alteration_check_button

    # Save button
    saveGuide_button = ttk.Button(button_frame2, text='Salvar guia', command=lambda: saveGuide())
    saveGuide_button.pack(side='top', pady=10, padx=10)
    saveGuide_button['state'] = 'disabled'

    # Choose button
    chooseGuide_button = ttk.Button(button_frame2, text='Carregar guia', command=lambda: chooseGuide())
    chooseGuide_button.pack(side='top', pady=10, padx=10)

    # Cancel button
    cancel_button = ttk.Button(button_frame2, text='Cancelar', command=lambda: cancel())
    cancel_button.pack(side='bottom', pady=10, padx=10)
    cancel_button['state'] = 'disabled'

    # Alteration button
    doAlteration_button = ttk.Button(button_frame, text='Realizar alterações', command=lambda: doAlteration())
    doAlteration_button.pack(side='right', pady=10, padx=10)
    doAlteration_button['state'] = 'disabled'

    # Alterations modes
    data_alteration_check_button = ttk.Checkbutton(window, text='Alteração de dados', variable="data_alteration_check")
    data_alteration_check_button.place(x=260, y=30)
    data_alteration_check_button['state'] = 'disabled'

    value_alteration_check_button = ttk.Checkbutton(window, text='Alteração de valores',
                                                    variable="value_alteration_check")
    value_alteration_check_button.place(x=260, y=50)
    value_alteration_check_button['state'] = 'disabled'

    # Generate hash button
    generateHashAndSave_button = ttk.Button(button_frame, text='Gerar hash', command=lambda: saveGuide())
    generateHashAndSave_button.pack(side='left', pady=10, padx=0)
    generateHashAndSave_button['state'] = 'disabled'

    openPlan_button = ttk.Button(window, text='Abrir planilha de\n alterações')
    openPlan_button.place(y=10, x=2)

    return window


def disableButtons(button_list):
    for button in button_list:
        button['state'] = 'disabled'


def enableButtons(button_list):
    for button in button_list:
        button['state'] = 'active'


def waitingOperation():
    chooseGuide_button['state'] = 'disabled'
    button_list = [doAlteration_button, generateHashAndSave_button, cancel_button,
                   value_alteration_check_button, data_alteration_check_button]
    enableButtons(button_list)


def cancel():
    chooseGuide_button['state'] = 'active'
    button_list = [generateHashAndSave_button, doAlteration_button, cancel_button,
                   data_alteration_check_button, value_alteration_check_button]
    data_alteration_check_button.deselect(), value_alteration_check_button.deselect()
    disableButtons(button_list)


def chooseGuide():
    global guide_path, tiss_guide, root_tag
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guide_path = fd.askopenfilename(filetypes=file_type)
    tiss_guide = ET.parse(guide_path, parser=ET.XMLParser(encoding="ISO-8859-1"))
    root_tag = tiss_guide.getroot()
    if guide_path != '':
        waitingOperation()
    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


def doAlteration():
    data_alteration_check = data_alteration_check_button.getvar('data_alteration_check')
    value_alteration_check = value_alteration_check_button.getvar('value_alteration_check')


window = createGui()
window.mainloop()