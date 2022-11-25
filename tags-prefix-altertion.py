import xml.etree.ElementTree as ET

ANS_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}  # SET TAG PREFIX USED AS DEFAULT BY TISS GUIDES
source_folder_path = 'C:/Users/eliasp/OneDrive - Fundação Faculdade de Medicina/altera_xml/REFATORAR_ALTERA_XML/sources'
TISS_guide = ET.parse(source_folder_path + '/GUIA_TESTE.xml')  # OPEN AND STORAGE TISS GUIDE IN VARIABLE
root_tag = TISS_guide.getroot()

path = source_folder_path

TISS_guide.write(path + '/GUIA_TESTE.xml', encoding="ISO-8859-1",  default_namespace=ANS_prefix['ans'], method='xml')

all_tags = root_tag.iter()

for i in all_tags:
    i.tag.replace('{http://www.ans.gov.br/padroes/tiss/schemas}', 'ans:')

TISS_guide.write(path + '/GUIA_TESTE.xml', encoding="ISO-8859-1",  default_namespace=ANS_prefix['ans'], method='xml')


