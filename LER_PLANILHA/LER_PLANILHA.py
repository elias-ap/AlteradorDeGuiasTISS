import pandas as pd

'''
SEÇÃO PARA LEITURA DAS CRITÍCAS EM UMA PLANILHA EXCEL
'''
tabela = pd.read_excel("PLANILHA_TESTE.xlsx") # LE A PLANILHA EM EXCEL
linhasTabela = len(tabela.index)  # QUANTIDADE DE LINHAS
colunasTabela = len(tabela.columns)  # QUANTIDADE DE COLUNAS
tabela = tabela.convert_dtypes(convert_string=True)  # CONVERTE A TABELA PARA TIPO STRING
tabela = tabela.fillna(5)  # FILTRA VALORES NULOS (CASO EXISTAM), TROCANDO OS PELO NÚMERO 5

listaDeCriticas = []
for i in range(0, linhasTabela):  # LOOP PARA CADA LINHA
    for j in range(0, colunasTabela):  # LOOP PARA CADA COLUNA
        listaDeCriticas.append(tabela.iloc[i][j])  # INSERE O REGISTRO DE CADA LINHA DA TABELA/CRITICA EM UMA LISTA
        if len(listaDeCriticas) == 11:
            for linha in listaDeCriticas:
                numeroConta = listaDeCriticas[0]
                deProcedimento = listaDeCriticas[1]
                paraProcedimento = listaDeCriticas[2]
                deTipoTabela = listaDeCriticas[3]
                paraTipoTabela = listaDeCriticas[4]
                deGrauPart = listaDeCriticas[5]
                paraGrauPart = listaDeCriticas[6]
                deCodigoDespesa = listaDeCriticas[7]
                paraCodigoDespesa = listaDeCriticas[8]
                deUnidadeMedida = listaDeCriticas[9]
                paraUnidadeMedida = listaDeCriticas[10]
                print(listaDeCriticas)
                listaDeCriticas.clear()
