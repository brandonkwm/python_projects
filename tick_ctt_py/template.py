from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.dom import minidom
import csv
import os
import shutil
import re

print('========Welcome to ticks CTT creater (entity ticks only)========')
while True:
     try:
         csv_fname_raw = input('Enter csv file name (without .csv extension): ')
         print(csv_fname_raw)
         csv_fname = csv_fname_raw.strip() #remove any leading/trailing white spaces
         print('...processing on '+csv_fname+'.csv')
         f = open(csv_fname+'.csv')
         break
     except FileNotFoundError:
         print('That file does not exist in the current directory '+os.getcwd()+'\nPlease try again')

csv_f = csv.reader(f, delimiter=';')
first_row = next(csv_f)


while True:
    try:
         xmlName_raw = input('please input your CTT name (w/o file extension): ')
         xmlName = xmlName_raw.strip() #remove any leading/trailing white spaces
         if set('[~!@#$%^&*+":;\']+$').intersection(xmlName):
              raise ValueError()
         else: break
    except ValueError:
        print('Special characters ~!@#$%^&*+":;\'+$ are not allowed' '\nPlease try again...')

root = Element('configuration-template',{'name':xmlName,'version':'v1.0'})
cfgItemName = SubElement(root,'configuration-item',{'name':'mx.accounting.Rule', 'object-id':'CM.201'})
instance = SubElement(cfgItemName,'instances')

for row in csv_f:
        instanceLabel= SubElement(instance,'instance',{'label':row[2]})
        instancePropLb = SubElement(instanceLabel,'instance-key',{'with-quotes':'true','property':'label'})
        instancePropLb.text = row[2]
        instancePropClass = SubElement(instanceLabel,'instance-key',{'property':'trnClass'})
        instancePropClass.text = row[3]
        instancePropFmly = SubElement(instanceLabel,'instance-key',{'with-quotes':'true','property':'trnFamily'})
        instancePropFmly.text = row[4]
        instancePropGrp = SubElement(instanceLabel,'instance-key',{'with-quotes':'true','property':'trnGroup'})
        instancePropGrp.text = row[5]
        instancePropTyp = SubElement(instanceLabel,'instance-key',{'with-quotes':'true','property':'trnType'})
        instancePropTyp.text = row[6]

#windows
cmf_templates = os.getcwd()+'\\cmf_templates' #os.getcwd() == 'C:\\Users\\Brandon\\AppData\\Local\\Programs\\Python\\Python36-32
#mac
#cmf_templates = os.getcwd()+'/cmf_templates'


if os.path.exists(cmf_templates):
    shutil.rmtree(cmf_templates)
os.makedirs(cmf_templates)
document = ElementTree(root)
document.write(xmlName+'.xml', encoding = 'utf-8',xml_declaration=True)
shutil.move(xmlName+'.xml',cmf_templates)

f.close()
