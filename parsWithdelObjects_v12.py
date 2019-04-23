import os
#import xml.etree.ElementTree as ET
import lxml.etree as et

folderObjects = r"C:\Users\User\Desktop\aaa\Object"
folderNewObjects = r"C:\Users\User\Desktop\aaa\Object2"

file_names = os.listdir(folderObjects)
dictionary_names = os.listdir(folderObjects)

len_mass = len(file_names)
len_mass_dictionary = len(dictionary_names)

i = 0
while i < len_mass_dictionary:
    if (dictionary_names[i].find("MV") or dictionary_names[i].find("SPS") or dictionary_names[i].find("DPS")\
        or dictionary_names[i].find("DPC")) and dictionary_names[i].find("Address") != -1 and dictionary_names[i].startswith("SCADA"):
        print('dictionary found: ', dictionary_names[i])
    else:
        del dictionary_names[i]
        len_mass_dictionary = len(dictionary_names)
        i-=1
    i+=1 


#if len(dictionary_names) != 4:
#    print(len(dictionary_names))
#    print('ОШИБКА! Неправильное количество словарей')
#    raise SystemExit(1)


i = 0
while i < len_mass:
    if (file_names[i].startswith("MV") or file_names[i].startswith("SPS") or file_names[i].startswith("DPS")\
       or file_names[i].startswith("DPC")) and file_names[i].find("Address") == -1 and file_names[i].find("Prf") == -1 :
        print('file found ', file_names[i])
    else:
        del file_names[i]
        len_mass = len(file_names)
        i-=1
    i+=1      

def parsDict(dictionary, mass):
    mass.append(dictionary)
    inputDictionary = et.parse(folderObjects + '\\' + dictionary)
    rootD = inputDictionary.getroot()
    extID = ''
    
    for object_dictionary_i in rootD.xpath('//Object'):
        count = 0
        ID = object_dictionary_i.get('id')
        #print(ID)
        for attribute_dictionary_i in object_dictionary_i.findall('Attribute'):
            if attribute_dictionary_i.attrib.get('Name') == 'object address':
                #mass.append(extID.replace(object_dictionary_i.attrib.get('Name'), attribute_dictionary_i.attrib.get('Value'))  + '<|>' + attribute_dictionary_i.attrib.get('Value') + '<|>' + extID)
                mass.append(object_dictionary_i.attrib.get('Name') + '<|>' + attribute_dictionary_i.attrib.get('Value') + '<|>' + ID)
    


mass0 = []
mass1 = []
mass2 = []
mass3 = []
mass4 = []
if len(dictionary_names) >= 1:
    parsDict(dictionary_names[0], mass0)
if len(dictionary_names) >= 2:
    parsDict(dictionary_names[1], mass1)
if len(dictionary_names) >= 3:
    parsDict(dictionary_names[2], mass2)
if len(dictionary_names) >= 4:
    parsDict(dictionary_names[3], mass3)
if len(dictionary_names) >= 5:
    parsDict(dictionary_names[4], mass4)

#print(mass0, mass1, mass2, mass3, mass4)

def checkMass(target, idTartget, mass):
    i=1
    while i < len(mass):
        temp = str(mass[i].split('<|>')[-1])
        if temp == target:
            idTartget = idTartget.replace( str(mass[i].split('<|>')[0]), str(mass[i].split('<|>')[1]))
            #if temp == 'Scs-1.EthernetNetwork-1.UCA2Gtw-2.GtwProt-1.GtwSCADAMapping-1.GtwSCADASPSMapping-1.GtwSCADASPSAddress-173':
                #print (idTartget)
                #print(temp)
                #print(mass[i]) 
            return idTartget

        i+=1
    return idTartget

def replaceA(target, idTartget, mass0, mass1, mass2, mass3, mass4):
    tempTarger = checkMass(target, idTartget, mass0)
    if tempTarger != idTartget:
        return tempTarger
    tempTarger = checkMass(target, idTartget, mass1)
    if tempTarger != idTartget:
        return tempTarger
    tempTarger = checkMass(target, idTartget, mass2)
    if tempTarger != idTartget:
        return tempTarger
    tempTarger = checkMass(target, idTartget, mass3)
    if tempTarger != idTartget:
        return tempTarger
    tempTarger = checkMass(target, idTartget, mass4)
    if tempTarger != idTartget:
        return tempTarger
    return idTartget
    #return tempTarger
    
for name in file_names:
    inputFileD = et.parse(folderObjects+ '\\' + name)
    root = inputFileD.getroot()
    target = ''
    idTartget = ''
    
    for relation_i in root.xpath('//Relation'):
        for target_i in relation_i.findall('TargetObjectId'):
            if type(target_i.text) == str:
                target = target_i.text
        for id_i in relation_i.findall('TargetObjectExtId'):
            if type(id_i.text) == str:
                idTartget = id_i.text
            if not target == '' and not idTartget == '':# and id_i.text != idTartget:
                id_i.text = replaceA(target, idTartget, mass0, mass1, mass2, mass3, mass4)
    inputFileD.write(folderNewObjects+ '\\' + name)
    

#print(mass2)
'''
for a in mass0:
    if a.find('1.40.8') != -1:
        print('mass 0 Find D  ' + a)
for a in mass1:
    if a.find('1.40.8') != -1:
        print('mass 1 Find D  ' + a)
for a in mass2:
    if a.find('1.40.8') != -1:
        print('mass 2 Find D  ' + a)
for a in mass3:
    if a.find('1.40.8') != -1:
        print('mass 3 Find D  ' + a)
for a in mass4:
    if a.find('1.40.8') != -1:
        print('mass 4 Find D  ' + a)
'''


for name in file_names:
    inputFile = et.parse(folderNewObjects+ '\\' + name)
    root = inputFile.getroot()
    count=0
    tag=0
    for object_i in root.xpath('//Object'):
        for attribute_i in object_i.findall('Attribute'):
            if attribute_i.attrib.get('Name') == 'spare':
                if int(attribute_i.attrib.get('Value')) == 1:
                    object_i.getparent().remove(object_i)
                    tag+=1
        count+=1
    print (count, tag)

    inputFile.write(folderNewObjects+ '\\' + name)


