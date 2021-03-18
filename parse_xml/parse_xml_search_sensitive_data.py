import os
import xml.etree.ElementTree as ET

synonym_list = ['ENTITY','ENTITIES','ENT','CTP','COUNTERPART','COUNTERPARTS','COUNTERPARTY','BROKER','CIF','BIC','PBPFS','NAME','TRADER','USER','BENEFICIARY','BEN_LBL','DESTINATION','DEST','SOURCE','SRC','PORT','PORTFOLIO','PTF','PFLD','PARTY']

for root, dirs, files in os.walk(os.path.join(os.getcwd(),'files')):
    for xmlfile in files:
        tree = ET.parse(os.path.join(os.getcwd(),'files',xmlfile))
        root = tree.getroot()
        for elem in root.iter():
            if elem.tag.strip().upper() in synonym_list:
                print(elem.tag.upper().strip() + ' found file name: ' + xmlfile)