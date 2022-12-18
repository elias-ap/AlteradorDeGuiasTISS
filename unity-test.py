# IMPORTS
import xml.etree.ElementTree as ET
import os
import pandas as PD
import hashlib
import customtkinter as cTk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

# SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES
global ans_prefix
ans_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}


def openWorksheet():
    path = os.path.abspath('sources/Teste.xlsx')
    os.startfile(f"{path}")


def isExists(obj):
    if obj is not None:
        return True

    else:
        return False


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
    if new_table_type != '' and new_table_type != tag_table_type.text:
        if new_table_type == '0':
            tag_table_type.text.replace(str(table_type), str(new_table_type)).replace('0', '00')
            generateAlterationLog(altered_data, table_type, new_table_type)

        else:
            tag_table_type.text = str(new_table_type)
            generateAlterationLog(altered_data, table_type, new_table_type)


def alterProcedureCode(specified_procedure_data):
    tag_procedure_code = specified_procedure_data.find('ans:codigoProcedimento', ans_prefix)

    if new_procedure_code != '' and new_procedure_code != tag_procedure_code.text:
        tag_procedure_code.text = tag_procedure_code.text.replace(str(procedure_code), str(new_procedure_code))
        altered_data = 'código do procedimento'
        generateAlterationLog(altered_data, procedure_code, new_procedure_code)


def alterUnityMeasure(specified_procedure_data):
    tag_unity_measure = specified_procedure_data.find('ans:unidadeMedida', ans_prefix)

    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(
            len(tag_unity_measure.text), '0')

        altered_data = 'unidade de medida'
        generateAlterationLog(altered_data, unity_measure, new_unity_measure)


def recalculateAllTotalValues(difference):
    # GET ACCOUNT TOTAL VALUES TAGS
    account_total_values_tag = account.find('ans:valorTotal', ans_prefix)
    general_total_values_tag = account_total_values_tag.find('ans:valorTotalGeral', ans_prefix)

    for total_value in account_total_values_tag:
        # IF TOTAL VALUE LARGER THAN DIFFERENCE VALUE ALTER
        if total_value.text > difference:
            total_value.text = f'{float(total_value.text) - float(difference):.2f}'
            general_total_values_tag.text = f'{float(general_total_values_tag.text) - float(difference):.2f}'
            break


def alterValues(specified_procedure_data):
    # GET PROCEDURE VALUE
    unitary_value_tag = specified_procedure_data.find('ans:valorUnitario', ans_prefix)

    # IF PROCEDURE VALUE IS THE SAME AS READED
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
        if f'{float(old_procedure_total_value):.2f}' > f'{new_procedure_total_value:.2f}':
            value_difference = f'{float(old_procedure_total_value) - float(procedure_total_value_tag.text):.2f}'
        else:
            value_difference = f'{float(new_procedure_total_value) - float(old_procedure_total_value):.2f}'

    altered_data = 'valor unitário'
    generateAlterationLog(altered_data, unitary_value, new_unitary_value)
    recalculateAllTotalValues(value_difference)


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


def createLogFile(path):
    # GET ABSOLUTE PATH OF LOGS FOLDER
    log_folder_path = os.path.abspath(r'Logs')
    log_name = path.split("_")[0]
    log_name = log_name.rsplit('/', 1)[1]

    # IF HAVE A LOG OF SAME GUIDE OPEN LOG LIKE APPEND MODE ELSE CREATE NEW TXT FILE AS LOG
    if os.path.isfile(f'{log_folder_path}/{log_name}.txt'):
        log_file = open(f'{log_folder_path}/{log_name}.txt', 'a')

    else:
        log_file = open(f'{log_folder_path}/{log_name}.txt', 'x')
        log_file.write('---------------------------- LOG DE ALTERAÇÕES ----------------------------\n')

    # BEFORE WRITE CHECK IN LOG IF IT HAS REPEATED LINES IN ALTERATION LOG LIST, IF YES REMOVE THEM FROM LIST
    log_file_readable = open(f'{log_folder_path}/{log_name}.txt', 'r')
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

    # SAVE ALTERED GUIDE
    tiss_guide.write(guide_path.split('_')[0] + f'_{new_hash_code}.xml', encoding="ISO-8859-1")
    # createLogFile(guide_path)
    # mb.showinfo(message='Arquivo salvo!')
    # cancelAlteration()


def chooseGuide(path):
    global guide_path, tiss_guide, root_tag, control_var
    guide_path = path
    control_var = 0
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
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
        accounts = root_tag.iter(possibles_guide_type[0])
        guide_type = 'SADT'
        return accounts

    else:
        accounts = root_tag.iter(possibles_guide_type[1])
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


def getExecutedAndExpensesProcedures(guide_account):
    account_procedures_dict = {'Executed procedures': None, 'Expenses procedures': None}
    account_executed_procedures = guide_account.find('ans:procedimentosExecutados', ans_prefix)
    account_expense_procedures = guide_account.find('ans:outrasDespesas', ans_prefix)

    if isExists(account_executed_procedures):
        account_procedures_dict['Executed procedures'] = (account_executed_procedures)

    if isExists(account_expense_procedures):
        account_procedures_dict['Expenses procedures'] = (account_expense_procedures)

    return account_procedures_dict


def getAllAccountProcedures(guide_account):
    print('     Função: Executou getAllAccountProcedures(guide_account)')
    if guide_type == 'SADT' and guide_number != '':
        guide_account = guide_account.find(f'ans:cabecalhoGuia[ans:numeroGuiaPrestador="{guide_number}"]..', ans_prefix)
        if isExists(guide_account):
            all_account_procedures = getExecutedAndExpensesProcedures(guide_account)
            return all_account_procedures
    elif guide_type == 'SADT':
        all_account_procedures = getExecutedAndExpensesProcedures(guide_account)
        return all_account_procedures

    elif guide_type == 'HOSPITALIZATION':
        all_account_procedures = getExecutedAndExpensesProcedures(guide_account)
        return all_account_procedures


def searchForSpecifiedProcedure(account_executed_procedures, account_expenses_procedures):
    print('     Função: searchForSpecifiedProcedure(account_executed_procedures, account_expenses_procedures)')
    # IF ACCOUNT HAVE EXECUTED PROCEDURES TAG (procedimentosExecutados)
    if isExists(account_executed_procedures):
        for data in account_executed_procedures:
            # SEARCH IN ACCOUNT EXECUTED PROCEDURES TAG FOR SPECIFIED PROCEDURE CODE
            executed_procedure = data.find(f'ans:procedimentoExecutado[ans:codigoProcedimento="{procedure_code}"]..',
                                           ans_prefix)

            # IF ACCOUNT HAVE THE SPECIFIED PROCEDURE GET HIS DATA
            if isExists(executed_procedure):
                executed_procedure_data = executed_procedure.find('ans:procedimentoExecutado', ans_prefix)

                return executed_procedure_data

    # IF ACCOUNT HAVE EXPENSES PROCEDURES TAG (outrasDespesas)
    if isExists(account_expenses_procedures):
        for data in account_expenses_procedures:
            # SEARCH IN ACCOUNT EXPENSE PROCEDURES TAG FOR SPECIFIED PROCEDURE CODE
            expense_procedure = data.find(f'ans:servicosExecutados[ans:codigoProcedimento="{procedure_code}"]..',
                                          ans_prefix)

            # IF ACCOUNT HAVE THE SPECIFIED PROCEDURE GET HIS DATA
            if isExists(expense_procedure):
                expense_procedure_data = expense_procedure.find('ans:servicosExecutados', ans_prefix)
                return expense_procedure_data
        else:
            mb.showinfo('Info', message=f'Procedimento: {procedure_code} não foi encontrado na guia escolhida')


def getSpecifiedProcedureData(account):
    print('Função: getSpecifiedProcedureData(account)')
    procedures_executed_and_expenses = getAllAccountProcedures(account)
    specified_procedure_data = searchForSpecifiedProcedure(
        procedures_executed_and_expenses['Executed procedures'],
        procedures_executed_and_expenses['Expenses procedures'])

    return specified_procedure_data


def doDataAlteration(guide_accounts):
    global control_var
    global lines
    lines = 0
    # READ WORKSHEET TABLE OF DATA ALTERATION
    table_reviews = PD.read_excel("sources/Teste.xlsx", sheet_name='1', dtype=str, keep_default_na=False)
    print(f'Variável: Quantidade de linhas a serem lidas: {len(table_reviews.values)}')
    print(f'Variável: Tipo de guia: {guide_type}')
    # FOR EACH REVIEW LINE IN TABLE, IF THE CONDITIONS IS ATTENDED DOES ALTERATIONS
    for review_line in table_reviews.values:
        global guide_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure, new_unity_measure
        [guide_number, procedure_code, new_procedure_code, table_type, new_table_type, unity_measure,
         new_unity_measure] = returnReviewLine(review_line, 'data')
        ###########################################################
        lines += 1
        ###########################################################
        if guide_type == 'SADT':
            global account
            for account in guide_accounts:
                if guide_number != '':
                    specified_procedure_data = getSpecifiedProcedureData()
                    if specified_procedure_data is not None:
                        alterTableType(specified_procedure_data)
                        alterUnityMeasure(specified_procedure_data)
                        alterProcedureCode(specified_procedure_data)
                        control_var += 1
                        break
                else:
                    specified_procedure_data = getSpecifiedProcedureData()

                    if specified_procedure_data is not None:
                        alterTableType(specified_procedure_data)
                        alterUnityMeasure(specified_procedure_data)
                        alterProcedureCode(specified_procedure_data)
                        control_var += 1

        if guide_type == 'HOSPITALIZATION':
            print('entrou no if')
            for account in guide_accounts:
                specified_procedure_data = getSpecifiedProcedureData(account)
                print(procedure_code)
            # print(f'Encontrou o seguinte procedimento: {specified_procedure_data.find("ans:codigoProcedimento", ans_prefix).text}')
            #     # if specified_procedure_data is not None:
            #     #     alterTableType(specified_procedure_data)
            #     #     alterUnityMeasure(specified_procedure_data)
            #     #     alterProcedureCode(specified_procedure_data)
            #     #     control_var += 1


def doValueAlteration(guide_accounts):
    global control_var
    # READ WORKSHEET TABLE OF VALUE ALTERATION
    table_reviews = PD.read_excel("sources/Teste.xlsx", sheet_name='2', dtype=str,
                                  keep_default_na=False)

    # FOR EACH REVIEW LINE IN TABLE, IF THE CONDITIONS IS ATTENDED DOES ALTERATIONS
    for review_line in table_reviews.values:
        global guide_number, procedure_code, unitary_value, new_unitary_value
        [guide_number, procedure_code, unitary_value, new_unitary_value] = returnReviewLine(review_line, 'values')

        if guide_type == 'SADT':
            global account
            for account in guide_accounts:
                if guide_number != '':
                    specified_procedure_data = getSpecifiedProcedureData()

                    if specified_procedure_data is not None:
                        alterValues(specified_procedure_data)
                        control_var += 1
                        break

                else:
                    specified_procedure_data = getSpecifiedProcedureData()

                    if specified_procedure_data is not None:
                        alterValues(specified_procedure_data)
                        control_var += 1

        elif guide_type == 'HOSPITALIZATION':
            for account in guide_accounts:
                specified_procedure_data = getSpecifiedProcedureData()

                if specified_procedure_data is not None:
                    alterValues(specified_procedure_data)
                    control_var += 1


def doAlterationAction():
    global control_var
    data_alteration_check = 1 # data_alteration_check_button.get()
    value_alteration_check = 0 # value_alteration_check_button.get()
    guide_accounts = getGuideType()
    try:
        if data_alteration_check == 1:
            e = 1
            print('Try: Alteração de dados')
            doDataAlteration(guide_accounts)

        if value_alteration_check == 1:
            e = 2
            doValueAlteration(guide_accounts)
    except Exception as e:
        if e == 1:
            mb.showerror('Erro', f'''
            Ocorreu algum erro durante as alterações de dados:\n
            Código de procedimento(atual): {procedure_code}\n
            Valores lidos:\n
            Tipo de tabela(atual) --> {table_type}
            Tipo de tabela(novo) --> {new_table_type}
            Código de procedimento(novo) --> {new_procedure_code}
            Unidade de médida (atual) --> {unity_measure}
            Unidade de médida (novo) --> {new_unity_measure}''')

        elif e == 2:
            mb.showerror('Erro', f'''
            Ocorreu algum erro durante as alterações de valores:\n
            Código de procedimento: {procedure_code}\n
            Valores lidos:\n
            Valor unitário (atual) --> {unitary_value}
            Valor unitário (novo) --> {new_unitary_value}
            ''')

    if data_alteration_check == 0 and value_alteration_check == 0:
        mb.showwarning('Erro', 'Escolha o modo de alteração')

    # elif control_var > 0:
    #     for button in (alteration_button, value_alteration_check_button,
    #                    data_alteration_check_button, check_button_information):
    #         button.destroy()
    #
    #     global saveGuide_button
    #     saveGuide_button = cTk.CTkButton(frame, text='Salvar Guia', command=lambda: saveGuideAfterAlterations())
    #     saveGuide_button.pack(side='bottom', pady=5, padx=5)

    else:
        mb.showinfo('Atenção', 'Não foi realizada nenhuma alteração.')


def generateHashAndSave():
    file_type = (('XML files', '*.xml'), ('All files', '*.*'))
    guides_paths = fd.askopenfilenames(filetypes=file_type)
    if guides_paths != '':
        for guide in guides_paths:
            tiss_guide = ET.parse(guide, parser=ET.XMLParser(encoding="ISO-8859-1"))
            root_tag = tiss_guide.getroot()
            root_tag_without_hash_text = removeHashTextFromGuide(root_tag)
            all_guide_tags = root_tag_without_hash_text.iter()
            new_hash_code = generateNewHashCode(all_guide_tags)
            root_tag.find('ans:epilogo', ans_prefix).find('ans:hash', ans_prefix).text = new_hash_code
            tiss_guide.write(guide.split('_')[0] + f'_{new_hash_code}.xml', encoding="ISO-8859-1")

        if len(guides_paths) > 1:
            mb.showinfo('Info', 'Arquivos salvos!')
        else:
            mb.showinfo('Info', 'Arquivo salvo!')
    else:
        mb.showwarning(title='Erro', message='A guia não foi escolhida!')


def createRelativeButtons():
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
    main_window = cTk.CTk()
    cTk.CTk.iconbitmap(main_window, r'resources/icon.ico')
    main_window.geometry('300x260')
    main_window.title('Alterador de Guias TISS')
    main_window.eval('tk::PlaceWindow . center')
    main_window.maxsize(300, 260)

    # MAIN FRAME
    frame = cTk.CTkFrame(main_window)
    frame.pack(side='left', fill='both', padx=10, pady=10, expand=True)

    # DEFAULT BUTTON
    open_plan_button = cTk.CTkButton(frame, text='Abrir planilha', command=lambda: openWorksheet())
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
    cancel_button = cTk.CTkButton(frame, text='Cancelar', command=lambda: cancelAlteration())
    cancel_button.pack(side='bottom', pady=5, padx=5)

    check_button_information = cTk.CTkLabel(frame, text='Escolha os modos de alteração:')
    check_button_information.pack(side='top', pady=5, padx=5)

    alteration_button = cTk.CTkButton(frame, text='Realizar alterações', command=lambda: doAlterationAction())
    alteration_button.pack(side='bottom', pady=5, padx=5)

    data_alteration_check_button = cTk.CTkSwitch(frame, text='Alteração de dados', text_color='white')
    data_alteration_check_button.pack(pady=10, padx=5)

    value_alteration_check_button = cTk.CTkSwitch(frame, text='Alteração de valor', text_color='white')
    value_alteration_check_button.pack(side='top', padx=5, pady=10)


########################################################################################################################

chooseGuide(r'C:\Users\elias\Documents\GitHub\python-automatics-data-alterations-in-xml-file\tests\00000000000000000090_ba313cac6d8bf136fdc5f46e4fd26fc0.xml'.replace('\\', '/'))
doAlterationAction()

print(f'Variável: Quantidade de críticas lidas: {lines}')

saveGuideAfterAlterations()


# window = createGui()
# window.mainloop()

