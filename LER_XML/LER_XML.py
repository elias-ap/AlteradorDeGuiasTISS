import xml.etree.ElementTree as ET

'''
SEÇÃ0 PARA ABERTURA E LEITURA DO ARQUIVO XML
'''
# caminho = input('Digite o caminho da guia: ').replace('"', '') # ALIMENTA A VARIÁVEL COM O PATH/CAMINHO DO ARQUIVO
# guiaTiss = ET.parse(str(caminho)) # ABRE O ARQUIVO
arquivo = ET.parse('GUIA_TESTE.xml') # ABRE O ARQUIVO
prefixo = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'} # DEFINE O PREFIXO USADO NAS TAGS DA GUIA TISS

raiz = arquivo.getroot() # SELECIONA A RAIZ DO ARQUIVO(TAG PRINCIPAL)
print(raiz)
