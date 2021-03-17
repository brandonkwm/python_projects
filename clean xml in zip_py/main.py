import zipfile
import xml.etree.ElementTree as ET
import os
import shutil

print('========cleaning xml in zip=========')
while True:
     try:
         print('working directory '+os.getcwd())
         zip_file_name = input('Enter zip file name (without .zip extension): ')
         directory_to_extract_to = os.getcwd()
         zip_file_name = zip_file_name.strip() #remove any leading/trailing white spaces
         print('...working on '+zip_file_name+'.zip')
         break
     except FileNotFoundError:
         print('That file does not exist in the current directory '+os.getcwd()+'\nPlease try again')


#backup current zip file
shutil.copy(os.path.join(os.getcwd(),zip_file_name+'.zip'),os.path.join(os.getcwd(),zip_file_name+'_bkp.zip'))

#extract CTT
with zipfile.ZipFile(os.path.join(os.getcwd(),zip_file_name+'.zip'), 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)
os.remove(os.path.join(os.getcwd(),zip_file_name)+'.zip')
	
#append line to version.properties file
fVersionPropFile='version.properties'
with open(fVersionPropFile,'a+') as fVersionPropFileOpen:
    fVersionPropFileOpen.write('zip.new.format=YES \n')

#1) clean cmf_templates .xml file
cmf_template_file = os.path.join(os.getcwd(),'cmf_templates',zip_file_name+'.xml')
tree = ET.parse(cmf_template_file)
root = tree.getroot()
with open(cmf_template_file,'w') as cmf_template_fileOpen:
    for elem in tree.iter():
        if elem.attrib.get('name') == 'mx.statics.MxUserPolicy':
            tree.getroot().remove(elem)
    
tree.write(cmf_template_file,encoding = 'UTF-8',xml_declaration=True)

#2) extract all files in users.zip 
with zipfile.ZipFile(os.path.join(os.getcwd(),'users','users.zip'), 'r') as zip_users_ref:
    print('...working on users.zip')
    zip_users_ref.extractall(os.path.join(directory_to_extract_to,'users','temp'))
os.remove(os.path.join(os.getcwd(),'users','users.zip'))
	
#3) clean unzipped xml file by removing Policies tag
users_file = os.path.join(os.getcwd(),'users','temp','loginimpl.data.document.0')
users_tree = ET.parse(users_file)
users_root = users_tree.getroot()
unwantedTag = users_root.findall('.//Policies')
with open(users_file,'wb') as users_fileOpen:
     for elem in unwantedTag:
            users_tree.getroot().remove(elem)   
     users_tree.write(users_file, xml_declaration=False, encoding='UTF-8')  

#4) add Selector tag and add back .xml headers
parentTag = root.findall('User')
for elem in users_root.iter('User'):
	selectorTag = ET.SubElement(elem,'Selector')
	selectorTag.text = 'MX3-INT'
with open(users_file,'wb') as users_fileOpen:
	users_fileOpen.write(b'<?xml version="1.0"?>')
	users_fileOpen.write(b'<!DOCTYPE GuiRoot>')
	users_tree.write(users_fileOpen, xml_declaration=False, encoding='UTF-8')  
	
#5) create new zip CM.149.zip and replace users.zip
users_zip_obj = os.path.join(os.getcwd(),'users','CM.149.zip')
zNew_users_zip = zipfile.ZipFile(users_zip_obj,'w',zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(os.path.join(os.getcwd(),'users','temp')):
    for f in files:
        zNew_users_zip.write(os.path.join(root, f))
zNew_users_zip.close()

#6) re-zip all files for new CTT
CTT_obj = zip_file_name+'.zip'
zCTT_zip = zipfile.ZipFile(CTT_obj,'w',zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk('.\\users'):
    for f in files:
        zCTT_zip.write(os.path.join(root, f))
for root, dirs, files in os.walk('.\\cmf_templates'):
    for f in files:
        zCTT_zip.write(os.path.join(root, f))
zCTT_zip.write('version.properties',arcname='version.properties')

print('...'+CTT_obj+' created. OUTPUT PATH: '+ os.getcwd())
print('...original CTT backed up. NAME:' + CTT_obj+'_bkp.zip. OUTPUT PATH: '+os.getcwd())

#clean up current working directory#clean up current working directory
shutil.rmtree(os.path.join(os.getcwd(),'cmf_templates'),ignore_errors=True)
shutil.rmtree(os.path.join(os.getcwd(),'users'),ignore_errors=True)
os.remove('version.properties')
