import hashlib
import xml.etree.ElementTree as ET

source_folder_path = 'C:/Users/eliasp/OneDrive - Fundação Faculdade de Medicina/altera_xml/REFATORAR_ALTERA_XML/sources'
TISS_guide = ET.parse("C:/Users/eliasp/Downloads/00000000000000007220_DC67F775AD962F84DBFD914E456B73D5.xml")
root_tag = TISS_guide.getroot()

ANS_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES

root_tag.find('ans:epilogo', ANS_prefix).find('ans:hash', ANS_prefix).text = ''

all_tags = root_tag.iter()
list = []
string = ''

for item in all_tags:

    if item.tag == '{'+ANS_prefix['ans']+'}descricaoProcedimento' or item.tag == '{'+ANS_prefix['ans']+'}observacao' or item.tag == '{'+ANS_prefix['ans']+'}nomeBeneficiario' or item.tag == '{'+ANS_prefix['ans']+'}nomeContratado' or item.tag == '{'+ANS_prefix['ans']+'}indicacaoClinica' or item.tag == '{'+ANS_prefix['ans']+'}nomeProfissional':
        list.append(item.text)
    else:
        list.append(item.text.replace(' ','').replace("\n",''))

for i in list:
    string += i


print("http://www.ans.gov.br/padroes/tiss/schemas"+' '+ "http://www.ans.gov.br/padroes/tiss/schemas/tissV3_03_03.xsd" +  string)
teste = "http://www.ans.gov.br/padroes/tiss/schemas"+ string
h = hashlib.md5()
encodado = teste.encode()
h.update(encodado)
print(h.hexdigest())
