# IMPORTS
import hashlib
import xml.etree.ElementTree as ET
import pandas as PD

""" FUNCTIONS THAT WILL BE USED BY SOFTWARE """


def doDataAlteration(do_data_alteration):
    if do_data_alteration == '1':
        # READ PLAN OF DATA ALTERATION IN EXCEL
        table_reviews = PD.read_excel(p + "/PLANILHA_ALTERA_DESPESA.xlsx", sheet_name='1', dtype=str,
                                      keep_default_na=False)
        print(table_reviews)
        line_count = len(table_reviews.index)
        columns_count = len(table_reviews.columns)
        for i in range(0, line_count):
            for j in range(0, columns_count):
                # INSERT LINE OF CRITICAL IN A LIST
                reviews_list.append(table_reviews.iloc[i][j])
                if len(reviews_list) == 7:  # WHEN LINE IS COMPLETE
                    [account_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure,
                     new_unity_measure] = returnReviewLine(reviews_list)

                    reviews_list.clear()
                    accounts = root_tag.iter(
                        '{http://www.ans.gov.br/padroes/tiss/schemas}guiaSP-SADT')  # guiaSP-SADT, guiaResumoInternacao
                    for account in accounts:
                        if account_number != '':
                            account_procedures = searchAccountProcedures(account)
                            procedure_data = searchProcedureDataInProcedure(account_procedures)

                            if procedure_data is not None:
                                alterTableType()
                                alterUnityMeasure()
                                alterProcedureCode()

                        else:
                            all_procedures_in_guide = account.iterfind('ans:outrasDespesas/', ans_prefix)
                            procedure_data = searchProcedureDataInProcedure(all_procedures_in_guide)
                            if procedure_data is not None:
                                alterTableType()
                                alterUnityMeasure()
                                alterProcedureCode()
    do_data_alteration = 0


########################################################################################################################

def doValueAlteration():
    if do_value_alteration.lower() == 'yes' or do_value_alteration.lower() == 'y':
        return True

    elif do_value_alteration.lower() == 'no' or do_value_alteration.lower() == 'n':
        return False


########################################################################################################################

def returnReviewLine(list):
    # IF DEFINED FOR DOING DATA ALTERATIONS:
    if do_data_alteration == '1':
        return list[0], list[1], list[2], list[3], list[4], list[5], list[6]

    # IF DEFINED FOR DOING VALUE ALTERATIONS:
    elif do_value_alteration == '1':
        return list[0], list[1], list[2].replace(',', '.'), list[3].replace(',', '.')


########################################################################################################################

def isExists(obj):
    if obj is not None:
        return True
    else:
        return False


########################################################################################################################

def searchAccountProcedures(account):
    account = account.find(f'ans:cabecalhoGuia[ans:numeroGuiaPrestador="{account_number}"]..', ans_prefix)

    if isExists(account):
        account_procedures = account.find('ans:outrasDespesas', ans_prefix)
        return account_procedures
    else:
        return None


########################################################################################################################

def searchProcedureDataInProcedure(account):
    if isExists(account):
        for procedures in account:
            # SEARCH FOR PROCEDURE CODE SPECIFIED IN ALL PROCEDURES OF ACCOUNT:
            procedure = procedures.find(f'ans:servicosExecutados[ans:codigoProcedimento="{procedure_code}"]..',
                                        ans_prefix)
            if isExists(procedure):
                procedure_data = procedure.find('ans:servicosExecutados', ans_prefix)
                return procedure_data

    else:
        return None


########################################################################################################################

def alterTableType():
    altered_data = 'table type'
    tag_table_type = procedure_data.find('ans:codigoTabela', ans_prefix)
    if new_table_type != '' and new_table_type != tag_table_type.text:
        if new_table_type == 0:
            tag_table_type.text.replace(str(table_type), str(new_table_type)).replace('0', '00')
            generateAlterationLog(altered_data, table_type, new_table_type)

        else:
            tag_table_type.text = str(new_table_type)
            generateAlterationLog(altered_data, table_type, new_table_type)


########################################################################################################################

def alterProcedureCode():
    altered_data = 'procedure code'

    tag_procedure_code = procedure_data.find('ans:codigoProcedimento', ans_prefix)
    if new_procedure_code != '' and new_procedure_code != tag_procedure_code.text:
        tag_procedure_code.text = tag_procedure_code.text.replace(str(procedure_code), str(new_procedure_code))
        generateAlterationLog(altered_data, procedure_code, new_procedure_code)


########################################################################################################################

def alterUnityMeasure():
    altered_data = 'unity measure'
    tag_unity_measure = procedure_data.find('ans:unidadeMedida', ans_prefix)

    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(
            len(tag_unity_measure.text), '0')
        generateAlterationLog(altered_data, unity_measure, new_unity_measure)


########################################################################################################################

def alterValue():
    altered_data = 'unitary value'

    unitary_value_tag = procedure_data.find('ans:valorUnitario', ans_prefix)
    procedure_total_value_tag = procedure_data.find('ans:valorTotal', ans_prefix)
    current_procedure_total_value = procedure_total_value_tag.text
    if unitary_value_tag.text == unitary_value:
        executed_quantity = procedure_data.find('ans:quantidadeExecutada', ans_prefix).text
        unitary_value_tag.text = f'{float(new_unitary_value):.2f}'
        procedure_total_value_tag.text = f'{float(unitary_value_tag.text) * float(executed_quantity):.2f}'

        if current_procedure_total_value > procedure_total_value_tag.text:
            value_difference = f'{float(current_procedure_total_value) - float(procedure_total_value_tag.text):.2f}'
        else:
            value_difference = f'{float(procedure_total_value_tag.text) - float(current_procedure_total_value):.2f}'

        recalculateAllTotalValues(value_difference)
        generateAlterationLog(altered_data, unitary_value, new_unitary_value)


########################################################################################################################

def recalculateAllTotalValues(valueDifference):
    account_total_values_tag = account.find('ans:valorTotal', ans_prefix)
    general_total_values_tag = account_total_values_tag.find('ans:valorTotalGeral', ans_prefix)
    wasRecalculated = False
    for total_value in account_total_values_tag:
        if wasRecalculated == False:
            if total_value.text > valueDifference:
                total_value.text = f'{float(total_value.text) + float(valueDifference):.2f}'
                general_total_values_tag.text = f'{float(general_total_values_tag.text) + float(valueDifference):.2f}'
                wasRecalculated = True


########################################################################################################################

def generateAlterationLog(altered_data, old_value, new_value):
    old = old_value
    new = new_value
    if account_number != '':
        return print(f'Account:{account_number} Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')
    else:
        return print(f'Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')


########################################################################################################################

def removeHashTextFromGuide(root_tag):
    root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = ''
    return root_tag


########################################################################################################################

def generateNewHashCode(all_tags):
    tags_texts = []
    unique_line_string = ''
    for tag in all_tags:
        tags_texts.append(tag.text.replace("\n", ''))

    for i in tags_texts:
        unique_line_string += i

    h = hashlib.md5(unique_line_string.encode('iso-8859-1'))
    new_hash_code = h.hexdigest()
    return new_hash_code


########################################################################################################################

# def saveGuide():
#     answer = input('Save archive? Write Y (Yes) or N (No)')
#     if answer.lower() == 'yes' or answer.lower() == 'y':
#         root_tag = removeHashTextFromGuide(tiss_guide.getroot())
#         all_tags = root_tag.iter()
#         new_hash_code = generateNewHashCode(all_tags)
#         root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code
#         tiss_guide.write(guide.split('_')[0].__add__(f'_{new_hash_code}.xml'), encoding="ISO-8859-1")
#
#     elif answer.lower() == 'no' or answer.lower() == 'n':
#         return print("Archive don't saved")


########################################################################################################################
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
                   valueAlterationCheck_button, dataAlterationCheck_button]
    enableButtons(button_list)


def cancel():
    chooseGuide_button['state'] = 'active'
    button_list = [generateHashAndSave_button, doAlteration_button, cancel_button, dataAlterationCheck_button, valueAlterationCheck_button]
    dataAlterationCheck_button.deselect(), valueAlterationCheck_button.deselect()
    disableButtons(button_list)
    guide = ''


def chooseGuide():
    global tiss_guide
    global root_tag
    global guide
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guide = fd.askopenfilename(filetypes=file_type)
    if guide != '':
        waitingOperation()
        tiss_guide = ET.parse(guide, parser=ET.XMLParser(encoding="ISO-8859-1"))
        root_tag = tiss_guide.getroot()
    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


def saveGuide():
    root_tag = removeHashTextFromGuide(tiss_guide.getroot())
    all_tags = root_tag.iter()
    new_hash_code = generateNewHashCode(all_tags)
    root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code
    tiss_guide.write(guide.split('_')[0].__add__(f'_{new_hash_code}.xml'), encoding="ISO-8859-1")
    mb.Message('Arquivo salvo')


def doAlteration():
    do_data_alteration = dataAlterationCheck_button.getvar('do_alteration')
    do_value_alteration = valueAlterationCheck_button.getvar('do_value_alteration')
    doDataAlteration(do_data_alteration)


global do_data_alteration, do_value_alteration
do_data_alteration = 0
do_value_alteration = 0

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
dataAlterationCheck_button = ttk.Checkbutton(window, text='Alteração de dados', variable="do_alteration")
dataAlterationCheck_button.place(x=150, y=50)
dataAlterationCheck_button['state'] = 'disabled'

valueAlterationCheck_button = ttk.Checkbutton(window, text='Alteração de valores', variable="do_value_alteration")
valueAlterationCheck_button.place(x=150, y=30)
valueAlterationCheck_button['state'] = 'disabled'


ans_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES
source_folder_path = 'sources'
p = source_folder_path
reviews_list = []

if do_value_alteration == 1:
    # READ PLAN OF VALUES ALTERATIONS IN EXCEL
    table_reviews = PD.read_excel(p + "/PLANILHA_ALTERA_DESPESA.xlsx", sheet_name='2', dtype=str, keep_default_na=False)

    line_count = len(table_reviews.index)
    columns_count = len(table_reviews.columns)

    for i in range(0, line_count):
        for j in range(0, columns_count):
            # INSERT LINE OF CRITICAL IN A LIST
            reviews_list.append(table_reviews.iloc[i][j])
            if len(reviews_list) == 4:  # WHEN LINE IS COMPLETE
                [account_number, procedure_code, unitary_value, new_unitary_value] = returnReviewLine(reviews_list)
                reviews_list.clear()
                accounts = root_tag.iter('{http://www.ans.gov.br/padroes/tiss/schemas}guiaSP-SADT')
                for account in accounts:
                    if account_number != '':
                        account_procedures = searchAccountProcedures(account)
                        procedure_data = searchProcedureDataInProcedure(account_procedures)
                        if procedure_data is not None:
                            alterValue()
                    else:
                        all_procedures_in_guide = account.iterfind('ans:outrasDespesas/', ans_prefix)
                        procedure_data = searchProcedureDataInProcedure(all_procedures_in_guide)
                        if procedure_data is not None:
                            alterValue()
    do_value_alteration = 0

window.mainloop()

