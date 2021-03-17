from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.dom import minidom
import csv
import template


csv_file_graph = open(template.csv_fname+'.csv')
csv_file_read = csv.reader(csv_file_graph,delimiter=';')
first_row = next(csv_file_read)

root = Element('graph')
for row in csv_file_read:
        rootEnt = SubElement(root,'rootEntity') 
        rootEnt.text = 'mx.accounting.Rule [label = '+row[2]+',trnClass = '+row[3]+', trnFamily = '+row[4]+', trnGroup = '+row[5]+', trnType = '+row[6]+']'

#introduce dummy dependency so import of final CTT is successful
entMgmt = SubElement(root,'entitiesManagement')
entStatus = SubElement(entMgmt,'entity',{'status':'SUCCEEDED','id':'mx.accounting.AccountDynamic [M-OBS Bal-MX]'})
dispLabel = SubElement(entStatus,'displayLabel',{'classname':'mx.accounting.AccountDynamic'})
propName=SubElement(dispLabel,'propertyName')
propName.text='label'
value1=SubElement(dispLabel,'value')
propName.text='M-OBS Bal-MX'

csv_file_graph.seek(0)
first_row = next(csv_file_read)
for row in csv_file_read:
        entStatus2 = SubElement(entMgmt,'entity',{'status':'SUCCEEDED','id':'mx.accounting.Rule [label = '+row[2]+',trnClass = '+row[3]+', trnFamily = '+row[4]+', trnGroup = '+row[5]+', trnType = '+row[6]+']'})
        natId = SubElement(entStatus2,'naturalId',{'classname':'mx.accounting.Rule'})
        propName2 = SubElement(natId,'property',{'name':'label'})
        strVal = SubElement(propName2,'stringValue')
        strVal.text = row[2]
        propName3 = SubElement(natId,'property',{'name':'trnClass'})
        strVal2 = SubElement(propName3,'stringValue')
        strVal2.text = row[3]
        propName4 = SubElement(natId,'property',{'name':'trnFamily'})
        strVal3 = SubElement(propName4,'stringValue')
        strVal3.text = row[4]
        propName5 = SubElement(natId,'property',{'name':'trnGroup'})
        strVal4 = SubElement(propName5,'stringValue')
        strVal4.text = row[5]
        propName6 = SubElement(natId,'property',{'name':'trnType'})
        strVal5 = SubElement(propName6,'stringValue')
        strVal5.text = row[6]
        dependency = SubElement(entStatus2,'dependency')
        dependency.text = 'mx.accounting.AccountDynamic [M-OBS Bal-MX]'

document = ElementTree(root)
document.write('graph.xml', encoding = 'utf-8',xml_declaration=True)
        
csv_file_graph.close()
