# IMPORTS
import xml.etree.ElementTree as ET
import os
import pandas as PD
import hashlib
import customtkinter as cTk
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


def alterUnityMeasure():
    tag_unity_measure = procedure_data.find('ans:unidadeMedida', ans_prefix)
    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(
            len(tag_unity_measure.text), '0')
        altered_data = 'unity measure'
        generateAlterationLog(altered_data, unity_measure, new_unity_measure)


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

        altered_data = 'unitary value'
        generateAlterationLog(altered_data, unitary_value, new_unitary_value)
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


def generateAlterationLog(altered_data, old_value, new_value):
    if "alteration_log_list" not in globals():
        global alteration_log_list
        alteration_log_list = []

    old = old_value
    new = new_value
    if account_number != '':
        alteration_log_list.append(f'Account:{account_number} Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')
    else:
        alteration_log_list.append(f'Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')



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

    def createLogFile(guide_path):
        log_folder_path = os.path.abspath(r'Logs')
        log_name = guide_path.split("_")[0]
        log_name = log_name.rsplit('/', 1)[1]
        if os.path.isfile(f'{log_folder_path}/{log_name}.txt'):
            log_file = open(f'{log_folder_path}/{log_name}.txt', 'a')
        else:
            log_file = open(f'{log_folder_path}/{log_name}.txt', 'x')
            log_file.write('---------------------------- LOG DE ALTERAÇÕES ----------------------------\n')

        log_file_readable = open(f'{log_folder_path}/{log_name}.txt', 'r')

        for line in log_file_readable.readlines():
            if line.replace("\n", '') in alteration_log_list:
                alteration_log_list.remove(line.replace("\n",''))

        for alteration in alteration_log_list:
            log_file.write(alteration + '\n')

        log_file.close()

    root_tag = removeHashTextFromGuide(tiss_guide.getroot())
    all_tags = root_tag.iter()
    new_hash_code = generateNewHashCode(all_tags)
    root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code
    if type(guide_path) == str:
        tiss_guide.write(guide_path.split('_')[0] + f'_{new_hash_code}.xml', encoding="ISO-8859-1")
        createLogFile(guide_path)
        mb.showinfo(message='Arquivo salvo!')
        cancelAlteration()
    else:
        tiss_guide.write(guide.split('_')[0].__add__(f'_{new_hash_code}.xml'), encoding="ISO-8859-1")



def createDefaultButtons():
    global generateHashAndSave_button, chooseGuide_button

    generateHashAndSave_button = cTk.CTkButton(frame, text='Gerar hash', command=lambda: generateHashAndSave())
    generateHashAndSave_button.pack(side='bottom', pady=5, padx=5)

    chooseGuide_button = cTk.CTkButton(frame, text='Carregar Guia', command=lambda: chooseGuide())
    chooseGuide_button.pack(side='bottom', pady=5, padx=5)


def createGui():
    global frame, generateHashAndSave_button, chooseGuide_button

    # GUI COLOR CONFIG
    cTk.set_appearance_mode('dark')
    cTk.set_default_color_theme('green')

    # MAIN WINDOW
    window = cTk.CTk()
    cTk.CTk.iconbitmap(window, r'icon.ico')
    window.geometry('300x260')
    window.title('Alterador de Guias TISS')
    window.eval('tk::PlaceWindow . center')
    window.maxsize(300, 260)

    # MAIN FRAME
    frame = cTk.CTkFrame(window)
    frame.pack(side='left', fill='both', padx=10, pady=10, expand=True)

    # DEFAULT BUTTONS
    openPlan_button = cTk.CTkButton(frame, text='Abrir planilha', command=lambda: openPlan())
    openPlan_button.pack(side='bottom', pady=5, padx=5)

    createDefaultButtons()

    return window


def waitingAlterationConfig():
    global cancel_button, check_button_information, alteration_button, saveGuide_button, \
        data_alteration_check_button, value_alteration_check_button

    # BUTTONS AFTER CHOOSE GUIDE
    cancel_button = cTk.CTkButton(frame, text='Cancelar', command=lambda: cancelAlteration())
    cancel_button.pack(side='bottom', pady=5, padx=5)

    check_button_information = cTk.CTkLabel(frame, text='Escolha os modos de alteração:')
    check_button_information.pack(side='top', pady=5, padx=5)

    alteration_button = cTk.CTkButton(frame, text='Realizar alterações', command=lambda: doAlteration())
    alteration_button.pack(side='bottom', pady=5, padx=5)

    data_alteration_check_button = cTk.CTkSwitch(frame, text='Alteração de dados', text_color='white')
    data_alteration_check_button.pack(pady=10, padx=5)

    value_alteration_check_button = cTk.CTkSwitch(frame, text='Alteração de valor', text_color='white')
    value_alteration_check_button.pack(side='top', padx=5, pady=10)

    generateHashAndSave_button.destroy()
    chooseGuide_button.destroy()


def cancelAlteration():
    global chooseGuide_button, generateHashAndSave_button
    # REDEFINE BUTTONS
    if "saveGuide_button" not in globals():
        for button in (alteration_button, cancel_button, data_alteration_check_button, value_alteration_check_button,
                       check_button_information):
            button.destroy()
    else:
        for button in (saveGuide_button, cancel_button, data_alteration_check_button, value_alteration_check_button,
                       check_button_information):
            button.destroy()

    createDefaultButtons()


def chooseGuide():
    global guide_path, tiss_guide, root_tag

    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guide_path = fd.askopenfilename(filetypes=file_type)
    if guide_path != '':
        tiss_guide = ET.parse(guide_path, parser=ET.XMLParser(encoding="ISO-8859-1"))
        root_tag = tiss_guide.getroot()
        waitingAlterationConfig()

    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


def doAlteration():
    global control_var, saveGuide_button
    data_alteration_check = data_alteration_check_button.get()
    value_alteration_check = value_alteration_check_button.get()

    source_folder_path = 'sources'
    p = source_folder_path
    reviews_list = []

    control_var = 0

    def doDataAlteration():
        global control_var
        if data_alteration_check == 1:
            # READ PLAN OF DATA ALTERATION IN EXCEL
            table_reviews = PD.read_excel("Planilha de Críticas.xlsx", sheet_name='1', dtype=str,
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
            control_var += 1

    def doValueAlteration():
        global control_var
        if value_alteration_check == 1:
            # READ PLAN OF VALUES ALTERATIONS IN EXCEL
            table_reviews = PD.read_excel("Planilha de Críticas.xlsx", sheet_name='2', dtype=str,
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
            control_var += 1

    # try:
    e = 1
    doDataAlteration()
    e = 2
    doValueAlteration()
    # except Exception:
        # if e == 1:
        #     mb.showerror('Erro', 'Ocorreu algum erro durante as alterações de dados')


        # elif e == 2:
        #     mb.showerror('Erro', 'Ocorreu algum erro durante as alterações de valores')

    if data_alteration_check == 0 and value_alteration_check == 0:
        mb.showwarning('Erro', 'Escolha o modo de alteração')

    elif control_var > 0:
        alteration_button.destroy()
        saveGuide_button = cTk.CTkButton(frame, text='Salvar Guia', command=lambda: saveGuide())
        saveGuide_button.pack(side='bottom', pady=5, padx=5)

    else:
        mb.showinfo('Atenção', 'Não foi realizada nenhuma alteração.')

    value_alteration_check_button.deselect()
    data_alteration_check_button.deselect()


def openPlan():
    path = os.path.abspath('Planilha de Críticas.xlsx')
    os.startfile(f"{path}")


def generateHashAndSave():
    global guide_path, tiss_guide, root_tag, guide
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guide_path = fd.askopenfilenames(filetypes=file_type)
    if guide_path != '':
        for guide in guide_path:
            guide = guide
            tiss_guide = ET.parse(guide, parser=ET.XMLParser(encoding="ISO-8859-1"))
            saveGuide()

        if len(guide_path) > 1:
            mb.showinfo('Sucesso', 'Arquivos salvos!')
        else:
            mb.showinfo('Sucesso', 'Arquivo salvo!')
    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


########################################################################################################################

GUI = createGui()
GUI.mainloop()
