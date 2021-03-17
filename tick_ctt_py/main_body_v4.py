from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.dom import minidom
import csv
import template
import graph
import sys
import os
import zipfile
import shutil
from shutil import copyfile
import re
from datetime import datetime


fileOpen = open(template.csv_fname+'.csv')
csv_file = csv.reader(fileOpen,delimiter=';')
first_row = next(csv_file)

#windows
mx_acc_rule = os.getcwd()+'\\mx\\accounting\\Rule' #os.getcwd() == C:\\Users\\Brandon\\AppData\\Local\\Programs\\Python\\Python36-32
staticData = os.getcwd()+'\\static_data'

#mac
#mx_acc_rule = os.getcwd()+'/mx/accounting/Rule' #os.getcwd() == C:\\Users\\Brandon\\AppData\\Local\\Programs\\Python\\Python36-32
#staticData = os.getcwd()+'/static_data'

if os.path.exists(mx_acc_rule):
    shutil.rmtree(mx_acc_rule)

if os.path.exists(staticData):
    shutil.rmtree(staticData)

os.makedirs(mx_acc_rule)
os.makedirs(staticData)

for row in csv_file:
    root = Element('MxML')
    root.set('version', '1-1')
    #setting document properties - hardcoded values
    #start
    docProp = SubElement(root,'documentProperties')
    prodBy = SubElement(docProp,'producedBy')
    partyName = SubElement(prodBy,'partyName')
    partyName.text = 'UOB (Singapore)'
    user = SubElement(prodBy,'user')
    name = SubElement(user,'name')
    name.text ='CONFIG'
    group = SubElement(user,'group')
    group.text = 'CONFIG'
    sysDate = SubElement(docProp,'systemDate')
    sysDate.text = '20161129'
    accDate = SubElement(docProp,'accountingDate')
    accDate.text = '00000000'
    comDate=SubElement(docProp,'computerDate')
    comDate.text= '20170421'
    comTime=SubElement(docProp,'computerTime')
    comTime.text = '16:44:26'
    #end

    #setting accounting rule accessor values
    top = SubElement(root,'mxAccountingIRULESet')
    mxAccRuleId = SubElement(top,'mxAccountingIRULE' ,{'id':'mxAccountingIRULE_0'}) #mxAccountingIRULE needs to have variable identifier
    bizObjId = SubElement(mxAccRuleId,'businessObjectId',{'mefClass':'mxAccountingIRULE'})
    identifier = SubElement(bizObjId,'identifier')
    identifier.text = row[1]#'1106' #to read from .csv for dummy running number
    natIdentifiers = SubElement(bizObjId,'naturalIdentifiers')
    natIden = SubElement(natIdentifiers,'naturalIdentifier')
    accName = SubElement(natIden,'accessorName')
    accName.text = 'label'
    accVal = SubElement(natIden,'accessorValue')
    accVal.text= row[2]#'COM SWAP...' #to read from .csv for rule label
    natIden2 = SubElement(natIdentifiers,'naturalIdentifier')
    accName2 = SubElement(natIden2,'accessorName')
    accName2.text = 'trnClass'
    accVal2 = SubElement(natIden2,'accessorValue')
    accVal2.text= row[3] #'0' #to read from .csv for trn_class
    natIden3 = SubElement(natIdentifiers,'naturalIdentifier')
    accName3 = SubElement(natIden3,'accessorName')
    accName3.text = 'trnFamily'
    accVal3 = SubElement(natIden3,'accessorValue')
    accVal3.text= row[4]#'COM' #to read from .csv for trn_fmly
    natIden4 = SubElement(natIdentifiers,'naturalIdentifier')
    accName4 = SubElement(natIden4,'accessorName')
    accName4.text = 'trnGroup'
    accVal4 = SubElement(natIden4,'accessorValue')
    accVal4.text= row[5]#'SWAP' #to read from .csv for trn_grp
    natIden5 = SubElement(natIdentifiers,'naturalIdentifier')
    accName5 = SubElement(natIden5,'accessorName')
    accName5.text = 'trnType'
    accVal5 = SubElement(natIden5,'accessorValue')
    accVal5.text= row[6]#'' #to read from .csv for trn_type
    primSys = SubElement(bizObjId,'primarySystem')
    primSys.text = 'MX'
    dispLabel = SubElement(bizObjId,'displayLabel')
    dispLabel.text = row[2]
    userDef = SubElement(mxAccRuleId,'userDefinedField')
    fieldLab = SubElement(userDef,'fieldLabel')
    fieldLab.text = 'FilterDetails'
    mxAccFilterDet = SubElement(userDef,'mxAccountingIRULE_FilterDetails')
        ####!!!!!!!!to add loop to generate multiple fields for multiple entities
    y=0 ##counter value for column number storing accounting section
    i=8 #in csv, column 8 onwards contains additional entities/accounting sections
    z=0 ##counter for FIRST column storing accounting sections
    for column in row[i:]:
        if('UOB' in row[i]):
            mxAccFilterDet2 = SubElement(mxAccFilterDet,'mxAccountingIRULE_FILTER_DETAIL')
            bizObjId2 = SubElement(mxAccFilterDet2,'businessObjectId',{'mefClass':'mxAccountingIRULE_FILTER_DETAIL'})
            primSys2 = SubElement(bizObjId2,'primarySystem')
            primSys2.text = 'MX'
            userDef2 = SubElement(mxAccFilterDet2,'userDefinedField')
            fieldLab = SubElement(userDef2,'fieldLabel')
            fieldLab.text = 'FieldType'
            fieldVal = SubElement(userDef2,'fieldValue')
            fieldVal.text = '0'
            fieldTyp = SubElement(userDef2,'fieldType')
            fieldTyp.text = 'integer'
            userDef3 = SubElement(mxAccFilterDet2,'userDefinedField')
            fieldLab2 = SubElement(userDef3,'fieldLabel')
            fieldLab2.text = 'FieldValue' #not a typo - indeed it is the fieldLabel tag = FieldValue str
            fieldVal2 = SubElement(userDef3,'fieldValue')
            fieldVal2.text = row[i]
            fieldTyp2 = SubElement(userDef3,'fieldType')
            fieldTyp2.text = 'character'
            i=i+1
        else:
             y=i+1
             z=i
             break
    
    if y==0:
        pass
    else:
        for column in row[y:]:
           if (row[y]):
                mxAccFilterDet2 = SubElement(mxAccFilterDet,'mxAccountingIRULE_FILTER_DETAIL')
                bizObjId2 = SubElement(mxAccFilterDet2,'businessObjectId',{'mefClass':'mxAccountingIRULE_FILTER_DETAIL'})
                primSys2 = SubElement(bizObjId2,'primarySystem')
                primSys2.text = 'MX'
                userDef2 = SubElement(mxAccFilterDet2,'userDefinedField')
                fieldLab = SubElement(userDef2,'fieldLabel')
                fieldLab.text = 'FieldType'
                fieldVal = SubElement(userDef2,'fieldValue')
                fieldVal.text = '1' 
                fieldTyp = SubElement(userDef2,'fieldType')
                fieldTyp.text = 'integer'
                userDef3 = SubElement(mxAccFilterDet2,'userDefinedField')
                fieldLab2 = SubElement(userDef3,'fieldLabel')
                fieldLab2.text = 'FieldValue' #not a typo - indeed it is the fieldLabel tag = FieldValue str
                fieldVal2 = SubElement(userDef3,'fieldValue')
                fieldVal2.text = row[y]
                fieldTyp2 = SubElement(userDef3,'fieldType')
                fieldTyp2.text = 'character'
                y=y+1
            
                
    userDef4 = SubElement(mxAccRuleId,'userDefinedField')
    fieldLab3 = SubElement(userDef4,'fieldLabel')
    fieldLab3.text = 'Label'
    fieldVal3 = SubElement(userDef4,'fieldValue')
    fieldVal3.text = row[2]
    fieldTyp3 = SubElement(userDef4,'fieldType')
    fieldTyp3.text = 'character'
    userDef5 = SubElement(mxAccRuleId,'userDefinedField')
    fieldLab4 = SubElement(userDef5,'fieldLabel')
    fieldLab4.text = 'TrnEntity'
    fieldVal4 = SubElement(userDef5,'fieldValue')
    fieldVal4.text = row[7] #in csv, column 7 contains first entity i.e. UOB SG
    fieldTyp4 = SubElement(userDef5,'fieldType')
    fieldTyp4.text = 'character'

    ###############HERE, WE MUST ADD LOGIC FOR ACC SECTIONS###################
    userDef5 = SubElement(mxAccRuleId,'userDefinedField')
    fieldLab4 = SubElement(userDef5,'fieldLabel')
    fieldLab4.text = 'TrnSection'
    fieldVal4 = SubElement(userDef5,'fieldValue')
    if z==0:
      fieldVal4.text = ''
    else:
      fieldVal4.text = row[z] #in loop, this is the 1st encounter of acc section leading to break from loop
    fieldTyp4 = SubElement(userDef5,'fieldType')
    fieldTyp4.text = 'character'

    ##########################################################################
    docName = '['+row[2]+']''['+row[3]+']''['+row[4]+']''['+row[5]+']''['+row[6]+']''.xml'
    new_docName = docName.replace('/','{S}') #replacing fwd slash as it is not allowed in filename
    new_docName = new_docName.replace(':','{C}') #replacing fwd slash as it is not allowed in filename
    document = ElementTree(root)
    document.write(new_docName, encoding = 'utf-8',xml_declaration=True)
    shutil.move(new_docName,mx_acc_rule)



#close .csv file
fileOpen.close()

zfile = 'CM.201.zip'
fileZip = zipfile.ZipFile(zfile, 'w',zipfile.ZIP_DEFLATED)
fileZip.write('graph.xml')
# Adding files from directory 'mx'
for root, dirs, files in os.walk('mx'):
    for f in files:
        fileZip.write(os.path.join(root, f))
fileZip.close()

shutil.move('CM.201.zip',staticData)

zCTT = template.xmlName+'.zip'
print(os.getcwd())
zParentZip = zipfile.ZipFile(zCTT,'w',zipfile.ZIP_DEFLATED)
#get all files in cmf_templates  folder and place it in CTT
for root, dirs, files in os.walk('cmf_templates'):
    for f in files:
        zParentZip.write(os.path.join(root, f))
#get all files in static_data folder and place it in CTT
for root, dirs, files in os.walk('static_data'):
    for f in files:
        zParentZip.write(os.path.join(root, f))
    
#write new file = version.properties to workaround error message thrown by richclient
#values are hardcoded.
date_time = datetime.now()
fVersionPropFilePath = os.path.join(os.getcwd(),'version.properties')
fVersionPropFile = open(fVersionPropFilePath,'w') 
fVersionPropFile.write("#"+date_time.strftime('%b %d %Y, %H:%M:%S')+'\n')
fVersionPropFile.write('mx.build.id=5258014-200519-1154-4251579 \n')
fVersionPropFile.write('zip.new.format=YES \n')
fVersionPropFile.write('mx.internal.version=v3.1.33.9a.en')
fVersionPropFile.close()

zParentZip.write(os.path.join(os.getcwd(),'version.properties'),arcname='version.properties')
zParentZip.close()




cfgmgmt = os.getcwd()+'\\cfgmgmt' #windows
# cfgmgmt = os.getcwd()+'/cfgmgmt' #mac
if os.path.exists(cfgmgmt):
    print('creating '+zCTT+' in '+cfgmgmt) #if there is any existing file with same name, script will overwrite existing file
    shutil.copy(zCTT,cfgmgmt)

else:
    print('creating '+cfgmgmt)
    os.mkdir(cfgmgmt)
    shutil.copy(zCTT,cfgmgmt)

#clean up current working directory
shutil.rmtree('cmf_templates',ignore_errors=True)
shutil.rmtree('static_data',ignore_errors=True)
shutil.rmtree('mx',ignore_errors=True)
os.remove(zCTT)
os.remove('graph.xml')
os.remove('version.properties')


#SQL that should be used during scoping...:
#author: brandon wong
