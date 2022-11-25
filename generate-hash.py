import hashlib
import xml.etree.ElementTree as ET

# SET TAG PREFIX USED BY TISS AS DEFAULT
global ANS_prefix
ANS_prefix = {'ans': 'http://www.ans.gov.br/padroes/tiss/schemas'}


def openTissGuide(absolute_file_path):
    guide = ET.parse(absolute_file_path)
    return guide


def getRootTag(guide):
    root_tag = guide.getroot()
    return root_tag


def removeHashTextFromGuide(root_tag):
    root_tag.find('ans:epilogo', ANS_prefix).find('ans:hash', ANS_prefix).text = ''
    return root_tag


def getAllTags(root_tag):
    all_tags = root_tag.iter()
    return all_tags


file_path = '' # FILE PATH

guide = openTissGuide(file_path)
root_tag = getRootTag(guide)
root_tag = removeHashTextFromGuide(root_tag)
all_tags = getAllTags(root_tag)

# STORAGE VARIABLES
tags_texts = []
unique_line_string = ''

for tag in all_tags:
    tags_texts.append(tag.text.replace("\n", ''))

for i in tags_texts:
    unique_line_string += i

h = hashlib.md5(unique_line_string.encode('iso-8859-1'))
new_hash_code = h.hexdigest()





