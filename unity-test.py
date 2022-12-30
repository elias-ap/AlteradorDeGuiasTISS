# IMPORTS
import xml.etree.ElementTree as ET
import os
import pandas as pd
import hashlib
import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

# SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES
global ans_prefix
ans_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}


def openWorksheet():
    path = os.path.abspath('Sources/Teste.xlsx')
    os.startfile(f"{path}")


def generateAlterationLog(altered_data, old, new):
    if "alteration_log_list" not in globals():
        global alteration_log_list
        alteration_log_list = []

    if guide_number != '':
        log_line = f'Número da conta:{guide_number} Procedimento:{procedure_code} {altered_data}:{old} alterado para:{new}'
        alteration_log_list.append(log_line)

    else:
        log_line = f'Procedimento:{procedure_code} {altered_data}:{old} alterado para:{new}'
        alteration_log_list.append(log_line)


def alterTableType(specified_procedure_data):
    altered_data = 'tipo de tabela'
    tag_table_type = specified_procedure_data.find('ans:codigoTabela', ans_prefix)
    if not ET.iselement(tag_table_type):
        tag_table_type = specified_procedure_data.find('ans:procedimento/ans:codigoTabela', ans_prefix)

    if new_table_type != '' and new_table_type != tag_table_type.text:
        if new_table_type == '0':
            tag_table_type.text.replace(str(table_type), str(new_table_type)).replace('0', '00')
            generateAlterationLog(altered_data, table_type, new_table_type)

        else:
            tag_table_type.text = str(new_table_type)
            generateAlterationLog(altered_data, table_type, new_table_type)


def alterUnityMeasure(specified_procedure_data):
    tag_unity_measure = specified_procedure_data.find('ans:unidadeMedida', ans_prefix)

    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(
            len(tag_unity_measure.text), '0')

        altered_data = 'unidade de medida'
        generateAlterationLog(altered_data, unity_measure, new_unity_measure)


def alterProcedureCode(specified_procedure_data):
    tag_procedure_code = specified_procedure_data.find('ans:codigoProcedimento', ans_prefix)
    # IF NOT RETURN THE TAG
    if not ET.iselement(tag_procedure_code):
        tag_procedure_code = specified_procedure_data.find('ans:procedimento/ans:codigoProcedimento', ans_prefix)

    if new_procedure_code != '' and new_procedure_code != tag_procedure_code.text:
        tag_procedure_code.text = tag_procedure_code.text.replace(str(procedure_code), str(new_procedure_code))
        altered_data = 'código do procedimento'
        generateAlterationLog(altered_data, procedure_code, new_procedure_code)


def recalculateAllTotalValues(difference, account):
    # GET ACCOUNT TOTAL VALUES TAGS
    if guide_type == 'SADT':
        account_total_values_tag = account.find('ans:valorTotal', ans_prefix)
        general_total_values_tag = account_total_values_tag.find('ans:valorTotalGeral', ans_prefix)

    for total_value in account_total_values_tag:
        # IF TOTAL VALUE LARGER THAN DIFFERENCE VALUE ALTER
        if float(total_value.text) > float(difference):
            total_value.text = f'{float(total_value.text) - float(difference):.2f}'
            general_total_values_tag.text = f'{float(general_total_values_tag.text) - float(difference):.2f}'
            break


def alterValues(specified_procedure_data, account):
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
        generateAlterationLog(altered_data, unitary_value, new_unitary_value)
        recalculateAllTotalValues(value_difference, account)


def removeHashTextFromGuide(guide_root_tag):
    guide_root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = ''
    return guide_root_tag


def generateNewHashCode(all_tags):
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


def createLogFile(guide_name):
    # GET ABSOLUTE PATH OF LOGS FOLDER
    log_folder_path = os.path.abspath(r'Logs')
    guide_name = guide_name.split("_")[0]

    # IF HAVE A LOG OF SAME GUIDE OPEN LOG LIKE APPEND MODE ELSE CREATE NEW TXT FILE AS LOG
    if os.path.isfile(f'{log_folder_path}/{guide_name}.txt'):
        log_file = open(f'{log_folder_path}/{guide_name}.txt', 'a')

    else:
        log_file = open(f'{log_folder_path}/{guide_name}.txt', 'x')
        log_file.write('---------------------------- LOG DE ALTERAÇÕES ----------------------------\n')

    # BEFORE WRITE CHECK IN LOG IF IT HAS REPEATED LINES IN ALTERATION LOG LIST, IF YES REMOVE THEM FROM LIST
    log_file_readable = open(f'{log_folder_path}/{guide_name}.txt', 'r')
    for line in log_file_readable.readlines():
        if line.replace("\n", '') in alteration_log_list:
            alteration_log_list.remove(line.replace("\n", ''))

    for alteration in alteration_log_list:
        log_file.write(alteration + '\n')

    alteration_log_list.clear()
    log_file.close()


def saveGuideAfterAlterations():
    root_tag_without_hash_text = removeHashTextFromGuide(root_tag)
    all_guide_tags = root_tag_without_hash_text.iter()

    new_hash_code = generateNewHashCode(all_guide_tags)
    root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code

    guide_name = os.path.basename(guide_path).split("_")[0]
    path = guide_path.rsplit('\\', 1)[0]

    # SAVE ALTERED GUIDE
    output_path = r"C:\Users\elias\Documents\GitHub\python-automatics-data-alterations-in-xml-file\Tests\Output"
    tiss_guide.write(f'{output_path}\\{guide_name.split("_")[0]}_{new_hash_code}.xml', encoding="ISO-8859-1")
    createLogFile(guide_name)
    # mb.showinfo(message='Arquivo salvo!')
    # cancelAlteration()


def chooseGuide(path):
    global guide_path, tiss_guide, root_tag, control_var
    guide_path = path
    control_var = 0
    # file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    # guide_path = fd.askopenfilename(filetypes=file_type)
    if guide_path != '':
        tiss_guide = ET.parse(guide_path, parser=ET.XMLParser(encoding="ISO-8859-1"))
        root_tag = tiss_guide.getroot()
        # waitingAlterationConfig()

    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


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


def returnReviewLine(review_list, mode):
    # IF DEFINED FOR DOING DATA ALTERATIONS:
    if mode == 'data':
        return review_list[0], review_list[1], review_list[2], review_list[3], review_list[4], review_list[5], \
               review_list[6]

    # IF DEFINED FOR DOING VALUE ALTERATIONS:
    if mode == 'values':
        return review_list[0], review_list[1], review_list[2].replace(',', '.'), review_list[3].replace(',', '.')


def getExecutedProcedures(guide_account):
    account_executed_procedures = guide_account.find('ans:procedimentosExecutados', ans_prefix)
    return account_executed_procedures


def getExpenseProcedures(guide_account):
    account_expense_procedures = guide_account.find('ans:outrasDespesas', ans_prefix)
    return account_expense_procedures


def searchSpecifiedProcedureInExecutedOrExpensesProcedures(account_executed_procedures, account_expense_procedures):
    if ET.iselement(account_executed_procedures):
        specified_procedure = searchSpecifiedProcedureCodeInExecutedProcedures(account_executed_procedures)
        if len(specified_procedure) > 0:
            return specified_procedure

    if ET.iselement(account_expense_procedures):
        specified_procedure = searchSpecifiedProcedureCodeInExpenseProcedures(account_expense_procedures)
        if len(specified_procedure) > 0:
            return specified_procedure
    else:
        message = f'Procedimento: {procedure_code} não foi encontrado na guia: {guide_number};\n'
        not_found_items.append(message)


def searchSpecifiedProcedureCodeInExecutedProcedures(procedures):
    # SEARCH IN ALL EXECUTED PROCEDURES FOR THE SPECIFIED PROCEDURE CODE
    procedure_data = procedures.iterfind(f'.//ans:procedimento[ans:codigoProcedimento="{procedure_code}"]..', ans_prefix)
    procedure_data = list(procedure_data)
    return procedure_data


def searchSpecifiedProcedureCodeInExpenseProcedures(procedures):
    # SEARCH IN ALL EXECUTED PROCEDURES FOR THE SPECIFIED PROCEDURE CODE
    procedure_data = procedures.iterfind(f'.//ans:servicosExecutados[ans:codigoProcedimento="{procedure_code}"].', ans_prefix)
    procedure_data = list(procedure_data)
    return procedure_data


def getSpecifiedProcedureData(guide_account):
    if guide_type == 'SADT' and guide_number != '':
        guide_account = guide_account.find(f'ans:cabecalhoGuia[ans:numeroGuiaPrestador="{guide_number}"]..', ans_prefix)
        if ET.iselement(guide_account):
            account_executed_procedures = getExecutedProcedures(guide_account)
            account_expense_procedures = getExpenseProcedures(guide_account)
            specified_procedure = searchSpecifiedProcedureInExecutedOrExpensesProcedures(account_executed_procedures,
                                                                                         account_expense_procedures)
            return specified_procedure

    elif guide_type == 'SADT' or guide_type == 'HOSPITALIZATION':
        account_executed_procedures = getExecutedProcedures(guide_account)
        account_expense_procedures = getExpenseProcedures(guide_account)
        specified_procedure = searchSpecifiedProcedureInExecutedOrExpensesProcedures(account_executed_procedures,
                                                                                     account_expense_procedures)
        return specified_procedure


def doDataAlteration(guide_accounts):
    global not_found_items
    # READ WORKSHEET TABLE OF DATA ALTERATION
    table_reviews = pd.read_excel("Sources/Teste.xlsx", sheet_name='1', dtype=str, keep_default_na=False)

    # FOR EACH REVIEW LINE IN TABLE, IF THE CONDITIONS IS ATTENDED DOES ALTERATIONS
    not_found_items = [f'Número de contas na guia: {len(guide_accounts)}\n']
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


def prepareDataAlteration(review_line):
    global guide_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure, new_unity_measure
    [guide_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure,
     new_unity_measure] = returnReviewLine(review_line, 'data')


def doValueAlteration(guide_accounts):
    global not_found_items
    # READ WORKSHEET TABLE OF VALUE ALTERATION
    table_reviews = pd.read_excel("Sources/Teste.xlsx", sheet_name='2', dtype=str,
                                  keep_default_na=False)

    not_found_items = [f'Número de contas na guia: {len(guide_accounts)}\n']
    # FOR EACH REVIEW LINE IN TABLE, IF THE CONDITIONS IS ATTENDED DOES ALTERATIONS
    for review_line in table_reviews.values:
        prepareValueAlteration(review_line)

        for account in guide_accounts:
            specified_procedure_data = getSpecifiedProcedureData(account)
            if isinstance(specified_procedure_data, list):
                for procedure in specified_procedure_data:
                    alterValues(procedure, account)
                    wasAltered()


def prepareValueAlteration(review_line):
    global guide_number, procedure_code, unitary_value, new_unitary_value
    [guide_number, procedure_code, unitary_value, new_unitary_value] = returnReviewLine(review_line, 'values')


def wasAltered():
    if "control_var" not in globals():
        global control_var
        control_var = 0

    control_var += 1


def doAlterationAction():
    data_alteration_check = 1 # data_alteration_check_button.get()
    value_alteration_check = 1 # value_alteration_check_button.get()
    guide_accounts = getGuideType()

    if data_alteration_check == 1:
        doDataAlteration(guide_accounts)

    if value_alteration_check == 1:
        doValueAlteration(guide_accounts)

    if data_alteration_check == 0 and value_alteration_check == 0:
        mb.showwarning('Erro', 'Escolha o modo de alteração')

    elif control_var > 0:
        print(f'Alterou:{control_var}')
        # for button in (alteration_button, value_alteration_check_button,
        #                data_alteration_check_button, check_button_information):
        #     button.destroy()
        #
        # global saveGuide_button
        # saveGuide_button = ctk.CTkButton(frame, text='Salvar Guia', command=lambda: saveGuideAfterAlterations())
        # saveGuide_button.pack(side='bottom', pady=5, padx=5)
        # saveGuideAfterAlterations()
    else:
        mb.showinfo('Atenção', 'Não foi realizada nenhuma alteração.')

    if len(not_found_items) > 1:
        message = ''
        for item in not_found_items:
            message += item
        mb.showinfo('Info', message)


def generateHashAndSave():
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guides_paths = fd.askopenfilenames(filetypes=file_type)
    if guides_paths != '':
        for guide_path in guides_paths:
            tiss_guide = ET.parse(guide_path, parser=ET.XMLParser(encoding="ISO-8859-1"))
            root_tag = tiss_guide.getroot()
            root_tag_without_hash_text = removeHashTextFromGuide(root_tag)
            all_guide_tags = root_tag_without_hash_text.iter()
            new_hash_code = generateNewHashCode(all_guide_tags)
            root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code

            guide_name = os.path.basename(guide_path).split("_")[0]
            path = guide_path.rsplit('/', 1)[0]

            tiss_guide.write(f'{path}/{guide_name}_{new_hash_code}.xml', encoding="ISO-8859-1")

        if len(guides_paths) > 1:
            mb.showinfo('Info', 'Arquivos salvos!')
        else:
            mb.showinfo('Info', 'Arquivo salvo!')
    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


def createRelativeButtons():
    global generateHashAndSave_button, chooseGuide_button

    generateHashAndSave_button = ctk.CTkButton(frame, text='Gerar hash', command=lambda: generateHashAndSave())
    generateHashAndSave_button.pack(side='bottom', pady=5, padx=5)

    chooseGuide_button = ctk.CTkButton(frame, text='Carregar Guia', command=lambda: chooseGuide())
    chooseGuide_button.pack(side='bottom', pady=5, padx=5)


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


def cancelAlteration():
    global control_var
    # REDEFINE BUTTONS
    if control_var == 0:
        for button in (alteration_button, cancel_button, data_alteration_check_button, value_alteration_check_button,
                       check_button_information):
            button.destroy()

    else:
        for button in (saveGuide_button, cancel_button):
            button.destroy()

    control_var = 0
    createRelativeButtons()


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


########################################################################################################################
# file_path = r"C:\Users\elias\Documents\GitHub\python-automatics-data-alterations-in-xml-file\Tests\00000000000000000090_ba313cac6d8bf136fdc5f46e4fd26fc0.xml"
file_path = r"C:\Users\elias\Documents\GitHub\python-automatics-data-alterations-in-xml-file\Tests\0001_a5fbec5215f9c66b4e9e7a4814f9c21e.xml"
chooseGuide(file_path)
doAlterationAction()
saveGuideAfterAlterations()


# window = createGui()
# window.mainloop()