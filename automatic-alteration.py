#   IMPORTS
import xml.etree.ElementTree as ET
import pandas as PD

"""                                 FUNCTIONS THAT WILL BE USED BY SOFTWARE                                          """


def doDataAlteration():
    if do_data_alteration.lower() == 'yes' or do_data_alteration.lower() == 'y':
        return True

    elif do_data_alteration.lower() == 'no' or do_data_alteration.lower() == 'n':
        return False


def doValueAlteration():
    if do_value_alteration.lower() == 'yes' or do_value_alteration.lower() == 'y':
        return True

    elif do_value_alteration.lower() == 'no' or do_value_alteration.lower() == 'n':
        return False


########################################################################################################################

#   FUNCTION TO RETURN THE CRITIC REVIEW LINE
def returnReviewLine(list):
    # IF DEFINED FOR DOING DATA ALTERATIONS:
    if doDataAlteration():
        return list[0], list[1], list[2], list[3], list[4], list[5], list[6]

    # IF DEFINED FOR DOING VALUE ALTERATIONS:
    elif doValueAlteration():
        return list[0], list[1], list[2].replace(',', '.'), list[3].replace(',', '.')


########################################################################################################################

#   FUNCTION TO CHECK IF A OBJECT EXISTS:
def isExists(obj):
    if obj is not None:
        return True
    else:
        return False


########################################################################################################################

#   FUNCTION FOR SEARCH ACCOUNTS IN GUIDE
def searchAccountProcedures(account):
    account = account.find(f'ans:cabecalhoGuia[ans:numeroGuiaPrestador="{account_number}"]..', ANS_prefix)

    if isExists(account):
        account_procedures = account.find('ans:outrasDespesas', ANS_prefix)
        return account_procedures
    else:
        return None


########################################################################################################################

#   FUNCTION FOR SEARCHING DATA OF THE SPECIFIED PROCEDURE IN ACCOUNT:
def searchProcedureDataInProcedure(account):
    if isExists(account):
        for procedures in account:
            # SEARCH FOR PROCEDURE CODE SPECIFIED IN ALL PROCEDURES OF ACCOUNT:
            procedure = procedures.find(f'ans:servicosExecutados[ans:codigoProcedimento="{procedure_code}"]..',
                                        ANS_prefix)
            if isExists(procedure):
                procedure_data = procedure.find('ans:servicosExecutados', ANS_prefix)
                return procedure_data

    else:
        return None


########################################################################################################################

#   FUNCTION FOR ALTER TABLE TYPE:
def alterTableType():
    altered_data = 'table type'
    tag_table_type = procedure_data.find('ans:codigoTabela', ANS_prefix)
    if new_table_type != '' and new_table_type != tag_table_type.text:
        if new_table_type == 0:
            tag_table_type.text.replace(str(table_type), str(new_table_type)).replace('0', '00')
            generateAlterationLog(altered_data, table_type, new_table_type)

        else:
            tag_table_type.text = str(new_table_type)
            generateAlterationLog(altered_data, table_type, new_table_type)


########################################################################################################################

#   FUNCTION FOR ALTER PROCEDURE CODE:
def alterProcedureCode():
    altered_data = 'procedure code'

    tag_procedure_code = procedure_data.find('ans:codigoProcedimento', ANS_prefix)
    if new_procedure_code != '' and new_procedure_code != tag_procedure_code.text:
        tag_procedure_code.text = tag_procedure_code.text.replace(str(procedure_code), str(new_procedure_code))
        generateAlterationLog(altered_data, procedure_code, new_procedure_code)


########################################################################################################################

#   FUNCTION FOR ALTER UNITY MEASURE
def alterUnityMeasure():
    altered_data = 'unity measure'
    tag_unity_measure = procedure_data.find('ans:unidadeMedida', ANS_prefix)

    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(
            len(tag_unity_measure.text), '0')
        generateAlterationLog(altered_data, unity_measure, new_unity_measure)


########################################################################################################################

#   FUNCTION FOR ALTER VALUE
def alterValue():
    altered_data = 'unitary value'

    unitary_value_tag = procedure_data.find('ans:valorUnitario', ANS_prefix)
    procedure_total_value_tag = procedure_data.find('ans:valorTotal', ANS_prefix)
    current_procedure_total_value = procedure_total_value_tag.text
    if unitary_value_tag.text == unitary_value:
        executed_quantity = procedure_data.find('ans:quantidadeExecutada', ANS_prefix).text
        unitary_value_tag.text = f'{float(new_unitary_value):.2f}'
        procedure_total_value_tag.text = f'{float(unitary_value_tag.text) * float(executed_quantity):.2f}'

        if current_procedure_total_value > procedure_total_value_tag.text:
            value_difference = f'{float(current_procedure_total_value) - float(procedure_total_value_tag.text):.2f}'
        else:
            value_difference = f'{float(procedure_total_value_tag.text) - float(current_procedure_total_value):.2f}'

        recalculateAllTotalValues(value_difference)
        generateAlterationLog(altered_data, unitary_value, new_unitary_value)


########################################################################################################################

#   FUNCTION FOR RECALCULATION TOTAL VALUES
def recalculateAllTotalValues(valueDifference):
    account_total_values_tag = account.find('ans:valorTotal', ANS_prefix)
    general_total_values_tag = account_total_values_tag.find('ans:valorTotalGeral', ANS_prefix)
    wasRecalculated = False
    for total_value in account_total_values_tag:
        if wasRecalculated == False:
            if total_value.text > valueDifference:
                total_value.text = f'{float(total_value.text) + float(valueDifference):.2f}'
                general_total_values_tag.text = f'{float(general_total_values_tag.text) + float(valueDifference):.2f}'
                wasRecalculated = True


########################################################################################################################

#   FUNCTION FOR GENERATE ALTERATION LOG:
def generateAlterationLog(altered_data, old_value, new_value):
    old = old_value
    new = new_value
    if account_number != '':
        return print(f'Account:{account_number} Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')
    else:
        return print(f'Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')


########################################################################################################################
"""
                                SECTION FOR OPENING AND READING OF ARCHIVE                                         

    Objective: Open archive/guide in format xml for read and realization of alterations

    Developer: Elias Araujo                                                                                            
    Date creation: 22/11/2022                                                        
"""

# guidePath = input('Digite o caminho da guia: ').replace('"', '') # SET GUIDE PATH
# TISSguide = ET.parse(str(guidePath)) # OPEN FILE

ANS_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES
source_folder_path = 'C:/Users/eliasp/OneDrive - Fundação Faculdade de Medicina/altera_xml/REFATORAR_ALTERA_XML/sources'
TISS_guide = ET.parse(source_folder_path + '/GUIA_TESTE.xml')  # OPEN AND STORAGE TISS GUIDE IN VARIABLE
root_tag = TISS_guide.getroot()

########################################################################################################################
"""
                                SECTION FOR READING CRITCS IN EXCEL PLAN                                       

    Objective:  Open a excel plan for read critics

    Developer: Elias Araujo                                                                                            
    Date creation: 22/11/2022        
"""

# TODO -> Why is looping two times if not have a for here? Fix it! -- FIXED
""" The bug happened because the logic of the functions was wrong """

p = source_folder_path

do_data_alteration = input('You want to do data alterations? Write Y(yes) or N(no):\n')
do_value_alteration = input('You want to do values alterations? Write Y(yes) or N(no):\n')

reviews_list = []
if doDataAlteration():
    # READ PLAN OF DATA ALTERATION IN EXCEL
    table_reviews = PD.read_excel(p + "/PLANILHA_ALTERA_DESPESA.xlsx", sheet_name='1', dtype=str, keep_default_na=False)

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
########################################################################################################################
                """
                                                SECTION FOR ACCOUNTS DATA ALTERATIONS IN GUIDE                                    

                    Objective:  Do data alterations in accounts accordingly with readed critic reviews

                    Developer: Elias Araujo                                                                                            
                    Date creation: 22/11/2022        
                """

                accounts = root_tag.iter('{http://www.ans.gov.br/padroes/tiss/schemas}guiaSP-SADT')
                for account in accounts:
                    if account_number != '':
                        account_procedures = searchAccountProcedures(account)
                        procedure_data = searchProcedureDataInProcedure(account_procedures)

                        if procedure_data is not None:
                            alterTableType()
                            alterUnityMeasure()
                            alterProcedureCode()

                    else:
                        all_procedures_in_guide = account.iterfind('ans:outrasDespesas/', ANS_prefix)
                        procedure_data = searchProcedureDataInProcedure(all_procedures_in_guide)
                        if procedure_data is not None:
                            alterTableType()
                            alterUnityMeasure()
                            alterProcedureCode()
    do_data_alteration = 'NO'
    TISS_guide.write(p + '/GUIA_TESTE.XML')

if doValueAlteration():
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
                """
                                                SECTION FOR ACCOUNTS DATA ALTERATIONS IN GUIDE                                    

                    Objective:  Do data alterations in accounts accordingly with readed critic reviews

                    Developer: Elias Araujo                                                                                            
                    Date creation: 22/11/2022        
                """
                accounts = root_tag.iter('{http://www.ans.gov.br/padroes/tiss/schemas}guiaSP-SADT')
                for account in accounts:
                    if account_number != '':
                        account_procedures = searchAccountProcedures(account)
                        procedure_data = searchProcedureDataInProcedure(account_procedures)
                        if procedure_data is not None:
                            alterValue()
                    else:
                        all_procedures_in_guide = account.iterfind('ans:outrasDespesas/', ANS_prefix)
                        procedure_data = searchProcedureDataInProcedure(all_procedures_in_guide)
                        if procedure_data is not None:
                            alterValue()

    do_value_alteration = 'NO'
    TISS_guide.write(p + '/GUIA_TESTE.XML')
