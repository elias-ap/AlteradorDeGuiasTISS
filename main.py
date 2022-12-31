# This Python file uses the following encoding: utf-8
# IMPORTS
import sys
import typing
import xml.etree.ElementTree as Et
import os
import pandas as pd
import hashlib
import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

# SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES
ans_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}

# CLOSE APPLICATION IF NOT IN RIGHT EXECUTION PATH
right_execution_path = r"O:\Informatica\Geral\Funcionais\Faturamento de Convênios\Alterador de Guias TISS"
current_execution_path = os.getcwd()
if current_execution_path != right_execution_path:
    mb.showwarning('Erro',
                   f'A aplicação só pode ser executada a partir do diretório original:\n{right_execution_path}')
    sys.exit()


def generateHashAndSave():
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guides_paths = fd.askopenfilenames(filetypes=file_type)
    if guides_paths != '':
        for path in guides_paths:
            # OPEN GUIDE
            root_tag = getRootTagFromXML(path)
            generateHash(root_tag)
            saveFile(path)

        if len(guides_paths) > 1:
            mb.showinfo('Info', 'Arquivos salvos!')
        else:
            mb.showinfo('Info', 'Arquivo salvo!')
    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


def openWorksheet():
    path = os.path.abspath('Planilha de Críticas.xlsx')
    os.startfile(f"{path}")


def openGuide():  # path: str
    global guide_path, root_tag
    # guide_path = path
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guide_path = fd.askopenfilename(filetypes=file_type)
    if os.path.isfile(guide_path):
        root_tag = getRootTagFromXML(guide_path)
        waitingAlterationConfig()

    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


def getRootTagFromXML(guide_path: str):
    global guide_file
    guide_file = Et.parse(guide_path, parser=Et.XMLParser(encoding="ISO-8859-1"))
    root_tag = guide_file.getroot()
    return root_tag


def waitingAlterationConfig():
    global cancel_button, check_button_information, alteration_button, saveGuide_button, \
        data_alteration_check_button, value_alteration_check_button

    # DESTROY RELATIVE BUTTONS
    generateHashAndSave_button.destroy()
    chooseGuide_button.destroy()

    # BUTTONS AFTER GUIDE CHOOSE
    cancel_button = ctk.CTkButton(frame, text='Cancelar', command=lambda: cancelAlteration())
    cancel_button.pack(side='bottom', pady=5, padx=5)

    check_button_information = ctk.CTkLabel(frame, text='Escolha os modos de alteração:')
    check_button_information.pack(side='top', pady=5, padx=5)

    alteration_button = ctk.CTkButton(frame, text='Realizar alterações', command=lambda: doAlterationAction())
    alteration_button.pack(side='bottom', pady=5, padx=5)

    data_alteration_check_button = ctk.CTkSwitch(frame, text='Alteração de dados', text_color='white')
    data_alteration_check_button.pack(pady=10, padx=5)

    value_alteration_check_button = ctk.CTkSwitch(frame, text='Alteração de valor', text_color='white')
    value_alteration_check_button.pack(side='top', padx=5, pady=10)


def doAlterationAction():
    global not_found_items, alteration_log_list, control_var
    control_var = 0
    alteration_log_list = []
    data_alteration_check = data_alteration_check_button.get()
    value_alteration_check = value_alteration_check_button.get()
    guide_accounts = getGuideType()
    not_found_items = [f'Número de contas na guia: {len(guide_accounts)}\n']

    if data_alteration_check == 1:
        doDataAlteration(guide_accounts)

    if value_alteration_check == 1:
        doValueAlteration(guide_accounts)

    if data_alteration_check == 0 and value_alteration_check == 0:
        mb.showwarning('Erro', 'Escolha o modo de alteração')

    elif control_var > 0:
        waitSave()
        global saveGuide_button
        saveGuide_button = ctk.CTkButton(frame, text='Salvar Guia', command=lambda: saveGuideAfterAlterations())
        saveGuide_button.pack(side='bottom', pady=5, padx=5)

    else:
        mb.showinfo('Atenção', 'Não foi realizada nenhuma alteração.')

    showNotFoundItems(not_found_items)


def getGuideType():
    global guide_type
    possibles_guide_type = '{' f'{ans_prefix["ans"]}' '}guiaSP-SADT', '{' f'{ans_prefix["ans"]}' '}guiaResumoInternacao'

    accounts = root_tag.iter(possibles_guide_type[0])
    if len(list(accounts)) > 0:
        accounts = list(root_tag.iter(possibles_guide_type[0]))
        guide_type = 'SADT'
        return accounts

    else:
        accounts = list(root_tag.iter(possibles_guide_type[1]))
        guide_type = 'HOSPITALIZATION'
        return accounts


def doDataAlteration(guide_accounts: list[Et.Element]):
    # READ WORKSHEET TABLE OF DATA ALTERATION
    table_reviews = pd.read_excel("Planilha de Críticas.xlsx", sheet_name='1', dtype=str, keep_default_na=False)

    # FOR EACH REVIEW LINE IN TABLE, IF THE CONDITIONS IS ATTENDED DOES ALTERATIONS
    for review_line in table_reviews.values:
        prepareDataAlteration(review_line)

        for account in guide_accounts:
            specified_procedure_data = getSpecifiedProcedureData(account)

            if isinstance(specified_procedure_data, list):
                for procedure in specified_procedure_data:
                    alterTableType(procedure)
                    alterUnityMeasure(procedure)
                    alterProcedureCode(procedure)
                    wasAltered()


def prepareDataAlteration(review_line: list):
    global guide_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure, new_unity_measure
    [guide_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure,
     new_unity_measure] = returnReviewLine(review_line, 'data')

    if new_table_type == '0':
        new_table_type = str(new_table_type).replace('0', '00')


def returnReviewLine(review_list: list, mode: str):
    # IF DEFINED FOR DOING DATA ALTERATIONS:
    if mode == 'data':
        return review_list[0], review_list[1], review_list[2], review_list[3], review_list[4], review_list[5], \
               review_list[6]

    # IF DEFINED FOR DOING VALUE ALTERATIONS:
    if mode == 'values':
        return review_list[0], review_list[1], review_list[2].replace(',', '.'), review_list[3].replace(',', '.')


def getSpecifiedProcedureData(guide_account: Et.Element):
    if guide_type == 'SADT' and guide_number != '':
        guide_account = guide_account.find(f'ans:cabecalhoGuia[ans:numeroGuiaPrestador="{guide_number}"]..', ans_prefix)
        if Et.iselement(guide_account):
            account_executed_procedures = getExecutedProcedures(guide_account)
            account_expense_procedures = getExpenseProcedures(guide_account)
            specified_procedure = searchSpecifiedProcedureInExecutedOrExpensesProcedures(account_executed_procedures,
                                                                                         account_expense_procedures)

            if specified_procedure is not None:
                return specified_procedure
            else:
                message = f'Procedimento: {procedure_code} não foi encontrado na conta: {guide_number}\n'
                not_found_items.append(message)

    elif guide_type == 'SADT' or guide_type == 'HOSPITALIZATION':
        account_executed_procedures = getExecutedProcedures(guide_account)
        account_expense_procedures = getExpenseProcedures(guide_account)
        specified_procedure = searchSpecifiedProcedureInExecutedOrExpensesProcedures(account_executed_procedures,
                                                                                     account_expense_procedures)
        if specified_procedure is not None:
            return specified_procedure
        else:
            account_number = guide_account.find(f'ans:cabecalhoGuia/ans:numeroGuiaPrestador', ans_prefix).text
            message = f'Procedimento: {procedure_code} não foi encontrado na conta: {account_number}\n'
            not_found_items.append(message)


def getExecutedProcedures(guide_account: Et.Element):
    account_executed_procedures = guide_account.find('ans:procedimentosExecutados', ans_prefix)
    return account_executed_procedures


def getExpenseProcedures(guide_account: Et.Element):
    account_expense_procedures = guide_account.find('ans:outrasDespesas', ans_prefix)
    return account_expense_procedures


def searchSpecifiedProcedureInExecutedOrExpensesProcedures(executed_procedures: Et.Element, expense_procedures: Et.Element):
    if Et.iselement(executed_procedures):
        specified_procedure = searchSpecifiedProcedureCodeInExecutedProcedures(executed_procedures)
        if len(specified_procedure) > 0:
            return specified_procedure

    if Et.iselement(expense_procedures):
        specified_procedure = searchSpecifiedProcedureCodeInExpenseProcedures(expense_procedures)
        if len(specified_procedure) > 0:
            return specified_procedure


def searchSpecifiedProcedureCodeInExecutedProcedures(procedures: Et.Element):
    # SEARCH IN ALL EXECUTED PROCEDURES FOR THE SPECIFIED PROCEDURE CODE
    procedure_data = procedures.iterfind(f'.//ans:procedimento[ans:codigoProcedimento="{procedure_code}"]..', ans_prefix)
    procedure_data = list(procedure_data)
    return procedure_data


def searchSpecifiedProcedureCodeInExpenseProcedures(procedures):
    # SEARCH IN ALL EXECUTED PROCEDURES FOR THE SPECIFIED PROCEDURE CODE
    procedure_data = procedures.iterfind(f'.//ans:servicosExecutados[ans:codigoProcedimento="{procedure_code}"].', ans_prefix)
    procedure_data = list(procedure_data)
    return procedure_data


def alterTableType(specified_procedure_data: Et.ElementTree):
    tag_table_type = specified_procedure_data.find('ans:codigoTabela', ans_prefix)

    if not Et.iselement(tag_table_type):
        tag_table_type = specified_procedure_data.find('ans:procedimento/ans:codigoTabela', ans_prefix)

    if new_table_type != '' and new_table_type != tag_table_type.text:
        tag_table_type.text = str(new_table_type)
        altered_data = 'tipo de tabela'
        prepareAlterationLogLines(altered_data, table_type, new_table_type)


def alterUnityMeasure(specified_procedure_data: Et.ElementTree):
    tag_unity_measure = specified_procedure_data.find('ans:unidadeMedida', ans_prefix)

    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(
            len(tag_unity_measure.text), '0')

        altered_data = 'unidade de medida'
        prepareAlterationLogLines(altered_data, unity_measure, new_unity_measure)


def alterProcedureCode(specified_procedure_data):
    if guide_type == 'SADT':
        tag_procedure_code = specified_procedure_data.find('ans:codigoProcedimento', ans_prefix)
    elif guide_type == 'HOSPITALIZATION':
        tag_procedure_code = specified_procedure_data.find('ans:procedimento/ans:codigoProcedimento', ans_prefix)

    if new_procedure_code != '' and new_procedure_code != tag_procedure_code.text:
        tag_procedure_code.text = tag_procedure_code.text.replace(str(procedure_code), str(new_procedure_code))
        altered_data = 'código do procedimento'
        prepareAlterationLogLines(altered_data, procedure_code, new_procedure_code)


def prepareAlterationLogLines(altered_data: str, old: str, new: str):
    if guide_number != '':
        log_line = f'Número da conta:{guide_number} Procedimento:{procedure_code} {altered_data}:{old} alterado para:{new} '
        alteration_log_list.append(log_line)

    else:
        log_line = f'Procedimento:{procedure_code} {altered_data}:{old} alterado para:{new}'
        alteration_log_list.append(log_line)


def wasAltered():
    global control_var
    control_var += 1


def doValueAlteration(guide_accounts):
    # READ WORKSHEET TABLE OF VALUE ALTERATION
    table_reviews = pd.read_excel("Planilha de Críticas.xlsx", sheet_name='2', dtype=str,
                                  keep_default_na=False)

    # FOR EACH REVIEW LINE IN TABLE, IF THE CONDITIONS IS ATTENDED DOES ALTERATIONS
    for review_line in table_reviews.values:
        prepareValueAlteration(review_line)

        for account in guide_accounts:
            specified_procedure_data = getSpecifiedProcedureData(account)
            if isinstance(specified_procedure_data, list):
                for procedure in specified_procedure_data:
                    alterValues(procedure, account)
                    wasAltered()


def prepareValueAlteration(review_line: list):
    global guide_number, procedure_code, unitary_value, new_unitary_value
    [guide_number, procedure_code, unitary_value, new_unitary_value] = returnReviewLine(review_line, 'values')


def alterValues(specified_procedure_data: Et.ElementTree, account: Et.ElementTree):
    # GET PROCEDURE UNITARY VALUE
    unitary_value_tag = specified_procedure_data.find('ans:valorUnitario', ans_prefix)

    # IF PROCEDURE VALUE IS THE SAME AS READED DOES ALTERATIONS
    if unitary_value_tag.text == f'{float(unitary_value):.2f}':
        executed_quantity = specified_procedure_data.find('ans:quantidadeExecutada', ans_prefix).text
        procedure_total_value_tag = specified_procedure_data.find('ans:valorTotal', ans_prefix)

        # STORAGE THE OLD PROCEDURE TOTAL VALUE
        old_procedure_total_value = procedure_total_value_tag.text

        # ALTER THE PROCEDURE UNITARY VALUE
        unitary_value_tag.text = f'{float(new_unitary_value):.2f}'

        # CALCULATE THE NEW TOTAL VALUE OF PROCEDURE AND ALTER
        new_procedure_total_value = f'{float(unitary_value_tag.text) * float(executed_quantity):.2f}'
        procedure_total_value_tag.text = new_procedure_total_value

        # IF OLD VALUE LARGER THAN NEW VALUE
        if f'{float(old_procedure_total_value):.2f}' > f'{float(new_procedure_total_value):.2f}':
            value_difference = f'{float(old_procedure_total_value) - float(procedure_total_value_tag.text):.2f}'
        else:
            value_difference = f'{float(new_procedure_total_value) - float(old_procedure_total_value):.2f}'

        altered_data = 'valor unitário'
        prepareAlterationLogLines(altered_data, unitary_value, new_unitary_value)
        recalculateAllTotalValues(value_difference, account)


def recalculateAllTotalValues(difference: str, account: Et.ElementTree):
    # GET ACCOUNT TOTAL VALUES TAGS
    account_total_values_tag = account.find('ans:valorTotal', ans_prefix)
    general_total_values_tag = account_total_values_tag.find('ans:valorTotalGeral', ans_prefix)

    for total_value in account_total_values_tag:
        # IF TOTAL VALUE LARGER THAN DIFFERENCE VALUE ALTER
        if float(total_value.text) > float(difference):
            total_value.text = f'{float(total_value.text) - float(difference):.2f}'
            general_total_values_tag.text = f'{float(general_total_values_tag.text) - float(difference):.2f}'
            break


def waitSave():
    for button in (alteration_button, value_alteration_check_button,
                   data_alteration_check_button, check_button_information):
        button.destroy()


def saveGuideAfterAlterations():
    # GENERATE NEW HASH
    generateHash(root_tag)

    # SAVE ALTERED GUIDE
    saveFile(guide_path)

    # GET GUIDE NAME
    guide_name = os.path.basename(guide_path).split("_")[0]
    createLogFile(guide_name)

    mb.showinfo(message='Arquivo salvo!')
    cancelAlteration()


def generateHash(root_tag: Et.Element):
    global new_hash_code
    root_tag_without_hash_text = removeHashTextFromGuide(root_tag)
    all_guide_tags = root_tag_without_hash_text.iter()
    new_hash_code = generateNewHashCode(all_guide_tags)
    root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code


def removeHashTextFromGuide(guide_root_tag: Et.Element):
    guide_root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = ''
    return guide_root_tag


def generateNewHashCode(all_tags: typing.Generator):
    tags_texts = []
    unique_line_string = ''
    # FOR EVERY TAG REMOVE LINE BREAKS
    for tag in all_tags:
        tags_texts.append(tag.text.replace("\n", ''))

    # FOR EVERY TEXT ADD TO UNIQUE LINE
    for text in tags_texts:
        unique_line_string += text

    # CREATE NEW HASH CODE
    h = hashlib.md5(unique_line_string.encode('iso-8859-1'))
    new_code = h.hexdigest()
    return new_code


def saveFile(guide_path: str):
    guide_name = os.path.basename(guide_path).split("_")[0]
    path = guide_path.rsplit('/', 1)[0]
    guide_file.write(f'{path}/{guide_name}_{new_hash_code}.xml', encoding="ISO-8859-1")


def createLogFile(guide_name: str):
    # GET ABSOLUTE PATH OF LOGS FOLDER
    log_folder_path = os.path.abspath(r'Logs')

    # IF HAVE A LOG OF SAME GUIDE OPEN LOG LIKE APPEND MODE ELSE CREATE NEW TXT FILE AS LOG
    log_file = checkIfExistsLogFile(guide_name, log_folder_path)

    # BEFORE WRITE CHECK IN LOG IF IT HAS REPEATED LINES IN ALTERATION LOG LIST, IF YES REMOVE THEM FROM LIST
    log_file_readable = open(f'{log_folder_path}/{guide_name}.txt', 'r')

    for line in log_file_readable.readlines():
        if line.replace("\n", '') in alteration_log_list:
            alteration_log_list.remove(line.replace("\n", ''))

    for alteration in alteration_log_list:
        log_file.write(alteration + '\n')

    alteration_log_list.clear()
    log_file.close()


def checkIfExistsLogFile(guide_name: str, log_folder_path: str):
    if os.path.isfile(f'{log_folder_path}/{guide_name}.txt'):
        log_file = open(f'{log_folder_path}/{guide_name}.txt', 'a')

    else:
        log_file = open(f'{log_folder_path}/{guide_name}.txt', 'x')
        log_file.write('---------------------------- LOG DE ALTERAÇÕES ----------------------------\n')
    return log_file


def showNotFoundItems(items: list):
    if len(items) > 1:
        message = ''
        for item in items:
            message += item
        mb.showinfo('Info', message)


def createGui():
    global frame, generateHashAndSave_button, chooseGuide_button

    # GUI COLOR CONFIG
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('green')

    # MAIN WINDOW
    main_window = ctk.CTk()
    ctk.CTk.iconbitmap(main_window, r'Resources/icon.ico')
    main_window.geometry('300x260')
    main_window.title('Alterador de Guias TISS')
    main_window.eval('tk::PlaceWindow . center')
    main_window.maxsize(300, 260)

    # MAIN FRAME
    frame = ctk.CTkFrame(main_window)
    frame.pack(side='left', fill='both', padx=10, pady=10, expand=True)

    # DEFAULT BUTTON
    open_plan_button = ctk.CTkButton(frame, text='Abrir planilha', command=lambda: openWorksheet())
    open_plan_button.pack(side='bottom', pady=5, padx=5)

    # RELATIVE BUTTONS
    createRelativeButtons()

    return main_window


def createRelativeButtons():
    global generateHashAndSave_button, chooseGuide_button

    generateHashAndSave_button = ctk.CTkButton(frame, text='Gerar hash', command=lambda: generateHashAndSave())
    generateHashAndSave_button.pack(side='bottom', pady=5, padx=5)

    chooseGuide_button = ctk.CTkButton(frame, text='Carregar Guia', command=lambda: openGuide())
    chooseGuide_button.pack(side='bottom', pady=5, padx=5)


def cancelAlteration():
    # REDEFINE BUTTONS
    if 'control_var' not in globals():
        for button in (alteration_button, cancel_button, data_alteration_check_button, value_alteration_check_button,
                       check_button_information):
            button.destroy()

    elif control_var > 0:
        for button in (saveGuide_button, cancel_button):
            button.destroy()

    createRelativeButtons()


########################################################################################################################

window = createGui()
window.mainloop()