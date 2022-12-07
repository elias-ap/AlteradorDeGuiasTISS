import tkinter as ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb


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
    button_list = [generateHashAndSave_button, doAlteration_button, cancel_button]
    disableButtons(button_list)


def chooseGuide():
    file_type = (('XML files', '*.xml'), ( 'All files', '*.*'))
    global guide
    guide = fd.askopenfilename(filetypes=file_type)
    if guide != '':
        waitingOperation()
    else:
        mb.showwarning(title='Erro' ,message='A guia não foi escolhida!')


def saveGuide():
    root_tag = removeHashTextFromGuide(tiss_guide.getroot())
    all_tags = root_tag.iter()
    new_hash_code = generateNewHashCode(all_tags)
    root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code
    tiss_guide.write(guide.split('_')[0].__add__(f'_{new_hash_code}.xml'), encoding="ISO-8859-1")


def doAlteration():
    do_alteration = data_alteration_check_button.getvar('do_alteration')
    do_value_alteration = value_alteration_check_button.getvar('do_value_alteration')

    return do_alteration, do_value_alteration

# Create window
window = ttk.Tk()
window.title('Alterador de guias TISS')
window.geometry('400x250')
window.eval('tk::PlaceWindow . center')

#       Create buttons

#   Button block
button_frame = ttk.Frame(window, background='blue')
button_frame.pack(side='bottom', pady=20, padx=20)

# Cancel button
cancel_button = ttk.Button(button_frame, text='Cancelar', command=lambda: cancel())
cancel_button.pack(side='right', pady=10, padx=10)
cancel_button['state'] = 'disabled'

# Choose button
chooseGuide_button = ttk.Button(button_frame, text='Carregar guia', command=lambda: chooseGuide())
chooseGuide_button.pack(side='right', pady=10, padx=10)

# Save button
saveGuide_button = ttk.Button(button_frame, text='Salvar guia')
saveGuide_button.pack(side='right', pady=10, padx=10)
saveGuide_button['state'] = 'disabled'

# Generate hash button
generateHashAndSave_button = ttk.Button(button_frame, text='Gerar hash', command=lambda: saveGuide())
generateHashAndSave_button.pack(side='top', pady=10, padx=10)
generateHashAndSave_button['state'] = 'disabled'

# Alteration button
doAlteration_button = ttk.Button(button_frame, text='Realizar alterações', command=lambda: doAlteration())
doAlteration_button.pack(side='top', pady=10, padx=10)
doAlteration_button['state'] = 'disabled'

# Alterations modes
data_alteration_check_button = ttk.Checkbutton(window, text='Alteração de dados', variable="do_alteration")
data_alteration_check_button.place(x=150, y=50)
data_alteration_check_button['state'] = 'disabled'

value_alteration_check_button = ttk.Checkbutton(window, text='Alteração de valores', variable="do_value_alteration")
value_alteration_check_button.place(x=150, y=30)
value_alteration_check_button['state'] = 'disabled'

window.mainloop()
