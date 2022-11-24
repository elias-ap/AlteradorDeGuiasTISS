import xml.etree.ElementTree as ET
import pandas as PD

from metodos import armazenaLinha, buscaVerificaConta, buscaProcedimentoNaConta, alteraTipoDeTabela,alteraProcedimento, alterarUnidadeDeMedida

'''
SEÇÃ0 PARA ABERTURA E LEITURA DO ARQUIVO XML
Abre o guiaTiss para leitura e realização das alterações.
'''
# caminhoDaGuia = input('Digite o caminho da guia: ').replace('"', '') # ALIMENTA A VARIÁVEL COM O PATH/CAMINHO DO ARQUIVO

# guiaTiss = ET.parse(str(caminhoDaGuia)) # ABRE O ARQUIVO

guiaTiss = ET.parse('GUIA_TESTE.xml')  # ABRE A GUIA TISS E O ARMAZENA NA VARIÁVEL

prefixoANS = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # DEFINE O prefixooANSO USADO NAS TAGS DA GUIA TISS

tagRaiz = guiaTiss.getroot()  # SELECIONA A RAIZ DO ARQUIVO(TAG PRINCIPAL)

'''
SEÇÃO PARA LEITURA DAS CRITÍCAS EM UMA PLANILHA EXCEL
Lê as critícas registrando cada linha em uma lista.
'''
# LE A PLANILHA EM EXCEL
tabelaDeCriticas = PD.read_excel("PLANILHA_ALTERA_DESPESA.xlsx", sheet_name='1')

QtdLinhas = len(tabelaDeCriticas.index)
QtdColunas = len(tabelaDeCriticas.columns)

# CONVERTE A TABELA PARA TIPO STRING E FILTRA VALORES VAZIOS
tabelaDeCriticas = tabelaDeCriticas.convert_dtypes(convert_floating=True, convert_string=True, convert_boolean=True)
tabelaDeCriticas = tabelaDeCriticas.fillna(5)  # FILTRA VALORES NULOS (CASO EXISTAM), TROCANDO OS PELO NÚMERO 5

listaDeCriticas = []
# LOOP PARA LEITURA DE CADA LINHA E COLUNA DA TABELA DE CRÍTICAS
for i in range(0, QtdLinhas):
    for j in range(0, QtdColunas):
        # INSERE O REGISTRO DE CADA LINHA DA TABELA/CRÍTICA EM UMA LISTA
        listaDeCriticas.append(tabelaDeCriticas.iloc[i][j])

        if len(listaDeCriticas) == 11:  # QUANDO ARMAZENAR TODA LINHA DE CRÍTICA ALIMENTA AS VARIÁVEIS:
            [numeroDaConta, deProcedimento, paraProcedimento, deTipoDeTabela, paraTipoDeTabela, deGrauDePart,
             paraGrauDePart, deCodigoDeDespesa, paraCodigoDeDespesa, deUnidadeDeMedida,
             paraUnidadeDeMedida] = armazenaLinha(listaDeCriticas)

            # LIMPA A LISTA
            listaDeCriticas.clear()

            '''
            SEÇÃO PARA AS ALTERAÇÕES DE DADOS DAS DESPESAS
            Para cada linha de critíca irá realizar uma busca nas guias da conta buscando 
            pelo número da conta e/ou procedimento especificado, alterando os dados de acordo com a critíca.
            '''
            guias = tagRaiz.iter('{http://www.ans.gov.br/padroes/tiss/schemas}guiaSP-SADT')
            for guia in guias:
                buscaVerificaConta(numeroDaConta, guia)
                for item in servicosExecutados:
                    # PARA CADA INFORMAÇÃO DO SERVICO EXECUTADO:
                    alteraTipoDeTabela(numeroDaConta, item, servicosExecutados, deProcedimento,
                                       deTipoDeTabela, paraTipoDeTabela)
                    alteraProcedimento(numeroDaConta, item, servicosExecutados, deProcedimento,
                                       paraProcedimento)
                    alterarUnidadeDeMedida(numeroDaConta, item, servicosExecutados, deProcedimento,
                                           deUnidadeDeMedida, paraUnidadeDeMedida)
        else:
            despesas = guia.iterfind('ans:outrasDespesas/', prefixoANS)
            for despesa in despesas:
                dadosDespesa = despesa.find(f'ans:servicosExecutados[ans:codigoProcedimento="{deProcedimento}"]..', prefixoANS)
                if dadosDespesa is not None:
                    servExec = dadosDespesa.find('ans:servicosExecutados', prefixoANS)
                    # PARA CADA ITEM/TAG DO SERVICO EXECUTADO
                    for item in servExec:
                        # VERIFICA O CODIGO DA TABELA PARA ALTERAR OU NÃO
                        if item.tag == servExec.find('.ans:codigoTabela', prefixoANS).tag and paraTipoDeTabela != 5:
                            if paraTipoDeTabela == 0:
                                item.text = str(paraTipoDeTabela).replace('0', '00')

                            else:
                                item.text = str(paraTipoDeTabela)
                        # VERIFICA O CODIGO DO PROCEDIMENTO PARA ALTERAR OU NÃO
                        if item.tag == servExec.find('.ans:codigoProcedimento',
                                                     prefixoANS).tag and paraProcedimento != 5:
                            item.text = item.text.replace(str(deProcedimento), str(paraProcedimento))
                        # VERIFICA A UNIDADE DE MEDIDA PARA ALTERAR OU NÃO
                        if item.tag == servExec.find('.ans:unidadeMedida', prefixoANS).tag and paraUnidadeDeMedida != 5:
                            item.text = str(paraUnidadeDeMedida).rjust(len(item.text), '0')

guiaTiss.write("GUIA_TESTE.xml")
