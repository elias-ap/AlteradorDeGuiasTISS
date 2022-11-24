#   VARIÁVEIS COMPLEMENTARES
global altered_data
ANS_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # PREFIXO GUIA TISS

########################################################################################################################
'''                                 FUNCTIONS THAT WILL BE USED BY SOFTWARE                                          '''


def doDataAlteration():
    from REFATORAR_ALTERA_XML.ALTERAR_DESPESA.ALTERA_DESPESA import do_data_alteration
    if do_data_alteration.lower() == 'yes' or 'y':
        return True

    elif do_data_alteration.lower() == 'no' or 'n':
        return False


def doValueAlteration():
    from REFATORAR_ALTERA_XML.ALTERAR_DESPESA.ALTERA_DESPESA import do_value_alteration
    if do_value_alteration.lower() == 'yes' or 'y':
        return True

    elif do_value_alteration.lower() == 'no' or 'n':
        return False


########################################################################################################################

#   FUNCTION TO RETURN THE CRITIC REVIEW LINE
def returnReviewLine(list):
    # IF DEFINED FOR DOING DATA ALTERATIONS:
    if doDataAlteration():
        return list[0], list[1], list[2], list[3], list[4], list[5], list[6]

    # IF DEFINED FOR DOING VALUE ALTERATIONS:
    elif doValueAlteration():
        return list[0], list[1], list[2], list[3]


########################################################################################################################

#   FUNCTION TO CHECK IF A OBJECT EXISTS:
def isExists(object):
    if object is not None:
        return True
    else:
        return False


########################################################################################################################

#   FUNCTION FOR SEARCH ACCOUNTS IN GUIDE
def searchAccountProcedures(account_number, guide):
    account = guide.find(f'ans:cabecalhoGuia[ans:numeroGuiaPrestador="{account_number}"]..', ANS_prefix)

    if isExists(account):
        account_procedures = account.find('ans:outrasDespesas', ANS_prefix)
        return account_procedures
    else:
        return None


########################################################################################################################

#   FUNCTION FOR SEARCHING DATA OF THE SPECIFIED PROCEDURE IN ACCOUNT:
def searchProcedureDataInProcedure(account, procedure_code):
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
    from REFATORAR_ALTERA_XML.ALTERAR_DESPESA.ALTERA_DESPESA import procedure_data, table_type, new_table_type

    tag_table_type = procedure_data.find('ans:codigoTabela', ANS_prefix)
    if new_table_type != '' and new_table_type != tag_table_type.text:
        if new_table_type == 0:
            tag_table_type.text.replace(str(table_type), str(new_table_type)).replace('0', '00')
            generateAlterLog(altered_data, table_type, new_table_type)

        else:
            tag_table_type.text = str(new_table_type)
            generateAlterLog(altered_data, table_type, new_table_type)


########################################################################################################################

#   FUNCTION FOR ALTER PROCEDURE CODE:
def alterProcedureCode():
    altered_data = 'procedure code'
    from REFATORAR_ALTERA_XML.ALTERAR_DESPESA.ALTERA_DESPESA import procedure_data, procedure_code, new_procedure_code

    tag_procedure_code = procedure_data.find('ans:codigoProcedimento', ANS_prefix)
    if new_procedure_code != '' and new_procedure_code != tag_procedure_code.text:
        tag_procedure_code.text = tag_procedure_code.text.replace(str(procedure_code), str(new_procedure_code))
        generateAlterLog(altered_data, procedure_code, new_procedure_code)


########################################################################################################################

#   FUNCTION PARA ALTERAR A UNIDADE DE MEDIDA
def alterUnityMeasure():
    altered_data = 'unity measure'
    tag_unity_measure = procedure_data.find('ans:unidadeMedida', ANS_prefix)
    if new_unity_measure != '' and new_unity_measure != tag_unity_measure.text:
        tag_unity_measure.text = tag_unity_measure.text.replace(str(unity_measure), str(new_unity_measure)).rjust(len(tag_unity_measure.text), '0')
        generateAlterLog(altered_data, unity_measure, new_unity_measure)
        return tag_unity_measure

########################################################################################################################

#   FUNCTION PARA ALTERAR VALOR
def alteraValor(guia, numeroDaConta, dadosProcedimento, deVlrUnitario, paraVlrUnitario):
    # ALIMENTA AS VARIÁVEIS COM OS DADOS NECESSÁRIOS PARA AS ALTERAÇÕES DE VALOR:
    codigoProcedimento = dadosProcedimento.find('ans:codigoProcedimento', ANS_prefix).text
    vlrUnitario = dadosProcedimento.find('ans:valorUnitario', ANS_prefix)
    vlrTotal = dadosProcedimento.find('ans:valorTotal', ANS_prefix)
    oldVlrTotal = vlrTotal.text

    # SE O VALOR ESTIVER DE ACORDO COM AS CRÍTICAS, REALIZA AS ALTERAÇÕES:
    if vlrUnitario.text == deVlrUnitario:
        qtdExecutada = dadosProcedimento.find('ans:quantidadeExecutada', ANS_prefix).text
        vlrUnitario.text = f'{float(paraVlrUnitario):.2f}'
        vlrTotal.text = f'{float(vlrUnitario.text) * float(qtdExecutada):.2f}'

        # PEGA DIFERENÇA DE VALORES E CHAMA A FUNÇÃO QUE FAZ O RECALCULO DOS VALORES TOTAIS:
        if oldVlrTotal > vlrTotal.text:
            valueDifference = f'{float(oldVlrTotal) - float(vlrTotal.text):.2f}'
        else:
            valueDifference = f'{float(vlrTotal.text) - float(oldVlrTotal):.2f}'
        recalculaVlrTotalGeral(guia, valueDifference)

        # LOG DAS ALTERAÇÕES:
        alteredData = 'valor unitário'
        generateAlterLog(numeroDaConta, codigoProcedimento, alteredData, deVlrUnitario, paraVlrUnitario)


########################################################################################################################

#   FUNCTION PARA RECALCULO DOS VALORES TOTAIS
def recalculaVlrTotalGeral(guia, valueDifference):
    valoresTotais = guia.find('ans:valorTotal', ANS_prefix)
    isRecalculated = False
    for total in valoresTotais:
        if isRecalculated == False:
            if total.text > valueDifference:
                total.text = f'{float(total.text) + float(valueDifference):.2f}'
                totalGeral = valoresTotais.find('ans:valorTotalGeral', ANS_prefix)
                totalGeral.text = f'{float(totalGeral.text) + float(valueDifference):.2f}'
                isRecalculated = True


########################################################################################################################

#   FUNCTION FOR GENERATE ALTERATION LOG:
def generateAlterLog(altered_data, old_value, new_value):
    old = old_value
    new = new_value
    from REFATORAR_ALTERA_XML.ALTERAR_DESPESA.ALTERA_DESPESA import account_number, procedure_code
    if account_number != '':
        return print(f'Account:{account_number} Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')
    else:
        return print(f'Procedure:{procedure_code} {altered_data}:{old} altered for:{new}')

########################################################################################################################
