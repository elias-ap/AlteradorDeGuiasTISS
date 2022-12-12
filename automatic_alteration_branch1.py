# IMPORTS
import xml.etree.ElementTree as ET
import os
import pandas as PD
import hashlib
import tkinter as ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

""" FUNCTIONS THAT WILL BE USED BY SOFTWARE """

global ans_prefix
ans_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES


def returnReviewLine(list, mode):
    # IF DEFINED FOR DOING DATA ALTERATIONS:
    if mode == 'data':
        return list[0], list[1], list[2], list[3], list[4], list[5], list[6]

    # IF DEFINED FOR DOING VALUE ALTERATIONS:
    if mode == 'values':
        return list[0], list[1], list[2].replace(',', '.'), list[3].replace(',', '.')


def isExists(obj):
    if obj is not None:
        return True
    else:
        return False


def searchAccountProcedures(conta):
    account = conta.find(f'ans:cabecalhoGuia[ans:numeroGuiaPrestador="{account_number}"]..', ans_prefix)
    if account is not None:
        account_procedures = account.find('ans:outrasDespesas', ans_prefix)

        return account_procedures
    else:
        return None


def searchProcedureDataInProcedure(account):
    if isExists(account):
        for procedures in account:
            # SEARCH FOR PROCEDURE CODE SPECIFIED IN ALL PROCEDURES OF ACCOUNT:
            procedure = procedures.find(f'ans:servicosExecutados[ans:codigoProcedimento="{procedure_code}"]..',
                                        ans_prefix)
            if isExists(procedure):
                global procedure_data
                procedure_data = procedure.find('ans:servicosExecutados', ans_prefix)
                return procedure_data

    else:
        return None


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


def alterProcedureCode():
    tag_procedure_code = procedure_data.find('ans:codigoProcedimento', ans_prefix)
    if new_procedure_code != '' and new_procedure_code != tag_procedure_code.text:
        tag_procedure_code.text = tag_procedure_code.text.replace(str(procedure_code), str(new_procedure_code))
        altered_data = 'procedure code'
        generateAlterationLog(altered_data, procedure_code, new_procedure_code)


########################################################################################################################

def alterUnityMeasure():
    tag_unity_measure = procedure_data.find('ans:unidadeMedida', ans_prefix)
    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(
            len(tag_unity_measure.text), '0')
        altered_data = 'unity measure'
        generateAlterationLog(altered_data, unity_measure, new_unity_measure)


########################################################################################################################

def alterValue():
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

    def recalculateAllTotalValues(valueDifference):
        account_total_values_tag = acnt.find('ans:valorTotal', ans_prefix)
        general_total_values_tag = account_total_values_tag.find('ans:valorTotalGeral', ans_prefix)
        wasRecalculated = False
        for total_value in account_total_values_tag:
            if wasRecalculated == False:
                if total_value.text > valueDifference:
                    total_value.text = f'{float(total_value.text) + float(valueDifference):.2f}'
                    general_total_values_tag.text = f'{float(general_total_values_tag.text) + float(valueDifference):.2f}'
                    wasRecalculated = True

        recalculateAllTotalValues(value_difference)
        altered_data = 'unitary value'
        generateAlterationLog(altered_data, unitary_value, new_unitary_value)


########################################################################################################################

def generateAlterationLog(altered_data, old_value, new_value):
    old = old_value
    new = new_value
    if account_number != '':
        return print(f'Account:{account_number} Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')
    else:
        return print(f'Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')


########################################################################################################################

def saveGuide():
    def removeHashTextFromGuide(root_tag):
        root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = ''
        return root_tag

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

    root_tag = removeHashTextFromGuide(tiss_guide.getroot())
    all_tags = root_tag.iter()
    new_hash_code = generateNewHashCode(all_tags)
    root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code
    tiss_guide.write(guide_path.split('_')[0].__add__(f'_{new_hash_code}.xml'), encoding="ISO-8859-1")

    cancel()
    saveGuide_button['state'] = 'disabled'
    mb.showinfo(message='Arquivo salvo!')


########################################################################################################################

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

    openPlan_button = ttk.Button(window, text='Abrir planilha de\n alterações', command=lambda: openPlan())
    openPlan_button.place(y=10, x=2)

    return window


########################################################################################################################

def chooseGuide():
    def waitingOperation():
        chooseGuide_button['state'] = 'disabled'
        button_list = [doAlteration_button, generateHashAndSave_button, cancel_button,
                       value_alteration_check_button, data_alteration_check_button]
        enableButtons(button_list)

    global guide_path, tiss_guide, root_tag
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guide_path = fd.askopenfilename(filetypes=file_type)
    tiss_guide = ET.parse(guide_path, parser=ET.XMLParser(encoding="ISO-8859-1"))
    root_tag = tiss_guide.getroot()
    if guide_path != '':
        waitingOperation()
    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')



########################################################################################################################

def disableButtons(button_list):
    for button in button_list:
        button['state'] = 'disabled'


########################################################################################################################

def enableButtons(button_list):
    for button in button_list:
        button['state'] = 'active'


########################################################################################################################

def cancel():
    chooseGuide_button['state'] = 'active'
    button_list = [generateHashAndSave_button, doAlteration_button, cancel_button,
                   data_alteration_check_button, value_alteration_check_button]
    data_alteration_check_button.deselect(), value_alteration_check_button.deselect()
    disableButtons(button_list)


########################################################################################################################

def doAlteration():
    data_alteration_check = data_alteration_check_button.getvar('data_alteration_check')
    value_alteration_check = value_alteration_check_button.getvar('value_alteration_check')

    source_folder_path = 'sources'
    p = source_folder_path
    reviews_list = []

    def doDataAlteration():
        if data_alteration_check == '1':
            # READ PLAN OF DATA ALTERATION IN EXCEL
            table_reviews = PD.read_excel(p + "/PLANILHA_ALTERA_DESPESA.xlsx", sheet_name='1', dtype=str,
                                          keep_default_na=False)

            line_count = len(table_reviews.index)
            columns_count = len(table_reviews.columns)
            for i in range(0, line_count):
                for j in range(0, columns_count):
                    # INSERT LINE OF CRITICAL IN A LIST
                    reviews_list.append(table_reviews.iloc[i][j])
                    if len(reviews_list) == 7:  # WHEN LINE IS COMPLETE
                        global account_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure, new_unity_measure
                        [account_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure,
                         new_unity_measure] = returnReviewLine(reviews_list, 'data')

                        reviews_list.clear()
                        global accounts
                        accounts = root_tag.iter(
                            '{http://www.ans.gov.br/padroes/tiss/schemas}guiaSP-SADT')  # guiaSP-SADT, guiaResumoInternacao
                        for account in accounts:
                            if account_number != '':
                                global account_procedures
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

    def doValueAlteration():
        if value_alteration_check == '1':
            # READ PLAN OF VALUES ALTERATIONS IN EXCEL
            table_reviews = PD.read_excel(p + "/PLANILHA_ALTERA_DESPESA.xlsx", sheet_name='2', dtype=str,
                                          keep_default_na=False)

            line_count = len(table_reviews.index)
            columns_count = len(table_reviews.columns)

            for i in range(0, line_count):
                for j in range(0, columns_count):
                    # INSERT LINE OF CRITICAL IN A LIST
                    reviews_list.append(table_reviews.iloc[i][j])
                    if len(reviews_list) == 4:  # WHEN LINE IS COMPLETE
                        global account_number, procedure_code, unitary_value, new_unitary_value
                        [account_number, procedure_code, unitary_value, new_unitary_value] = returnReviewLine(
                            reviews_list, 'values')
                        reviews_list.clear()
                        accounts = root_tag.iter('{http://www.ans.gov.br/padroes/tiss/schemas}guiaSP-SADT')

                        if accounts is None:
                            accounts = root_tag.iter('{http://www.ans.gov.br/padroes/tiss/schemas}guiaResumoInternacao')

                        for account in accounts:
                            global acnt
                            acnt = account
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

    try:
        e = 1
        doDataAlteration()
        data_alteration_check_button.deselect()
        e = 2
        doValueAlteration()
        value_alteration_check_button.deselect()

    except Exception:
        if e == 1:
            mb.showerror('Erro', 'Ocorreu algum erro durante as alterações de dados')
        elif e == 2:
            mb.showerror('Erro', 'Ocorreu algum erro durante as alterações de valores')

    saveGuide_button['state'] = 'active'

    if data_alteration_check == '0' and value_alteration_check == '0':
        mb.showwarning('Erro', 'Escolha o modo de alteração')


########################################################################################################################

def openPlan():
    os.system(command=os.PathLike())


########################################################################################################################

GUI = createGui()
GUI.mainloop()
