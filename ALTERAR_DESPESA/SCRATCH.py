import xml.etree.ElementTree as ET
import pandas as PD

from metodos import alteraProcedimento, alteraTipoDeTabela, alterarUnidadeDeMedida, armazenaLinha

'''
SEÇÃ0 PARA ABERTURA E LEITURA DO ARQUIVO XML
Abre o guiaTiss para leitura e realização das alterações.
'''
# caminhoDaGuia = input('Digite o caminho da guia: ').replace('"', '') # ALIMENTA A VARIÁVEL COM O PATH/CAMINHO DO ARQUIVO

# guiaTiss = ET.parse(str(caminho)) # ABRE O ARQUIVO

guiaTiss = ET.parse('GUIA_TESTE.xml')  # ABRE A GUIA TISS E O ARMAZENA NA VARIÁVEL

prefixoANS = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # DEFINE O PREFIXO USADO NAS TAGS DA GUIA TISS

tagRaiz = guiaTiss.getroot()  # SELECIONA A RAIZ DO ARQUIVO(TAG PRINCIPAL)

'''
SEÇÃO PARA LEITURA DAS CRITÍCAS EM UMA PLANILHA EXCEL
Lê as critícas registrando cada linha em uma lista.
'''
tabelaDeCriticas = PD.read_excel("PLANILHA_ALTERA_DESPESA.xlsx", sheet_name='1')  # LE A PLANILHA EM EXCEL

QtdLinhas = len(tabelaDeCriticas.index)

QtdColunas = len(tabelaDeCriticas.columns)

tabelaDeCriticas = tabelaDeCriticas.convert_dtypes(convert_string=True)  # CONVERTE A TABELA PARA TIPO STRING

tabelaDeCriticas = tabelaDeCriticas.fillna(5)  # FILTRA VALORES NULOS (CASO EXISTAM), TROCANDO OS PELO NÚMERO 5

listaDeCriticas = []

for i in range(0, QtdLinhas):       # LOOP PARA LEITURA DE CADA LINHA E COLUNA
    for j in range(0, QtdColunas):  # DA TABELA DE CRÍTICAS
        listaDeCriticas.append(tabelaDeCriticas.iloc[i][j])  # INSERE O REGISTRO DE CADA LINHA DA TABELA/CRíTICA EM UMA LISTA
        if len(listaDeCriticas) == 11:  # QUANDO ARMAZENAR TODA LINHA DE CRÍTICA ALIMENTA AS VARIÁVEIS
            [numeroDeConta, deProcedimento, paraProcedimento, deTipoTabela, paraTipoTabela, deGrauDePart,
             paraGrauDePart, deCodigoDeDespesa, paraCodigoDeDespesa, deUnidadeDeMedida,
             paraUnidadeDeMedida] = armazenaLinha(listaDeCriticas)

            print(numeroDeConta, deProcedimento, paraProcedimento, deTipoTabela, paraTipoTabela, deGrauDePart,
                  paraGrauDePart, deCodigoDeDespesa, paraCodigoDeDespesa, deUnidadeDeMedida, paraUnidadeDeMedida)
            # LIMPA A LISTA
            listaDeCriticas.clear()