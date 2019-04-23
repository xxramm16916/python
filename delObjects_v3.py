import os
#import xml.etree.ElementTree as ET
import lxml.etree as et

folderObjects = r"C:\Users\User\Desktop\работа\Pacis\словарь\Object"
folderNewObjects = r"C:\Users\User\Desktop\работа\Pacis\словарь\Object1"

file_names = os.listdir(folderObjects)
dictionary_names = os.listdir(folderObjects)

len_mass = len(file_names)
len_mass_dictionary = len(dictionary_names)

i = 0
while i < len_mass_dictionary:
    if (dictionary_names[i].find("MV") or dictionary_names[i].find("SPS") or dictionary_names[i].find("DPS") or dictionary_names[i].find("DPC")) and dictionary_names[i].find("Address") != -1:
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
    if file_names[i].startswith("MV") or file_names[i].startswith("SPS") or file_names[i].startswith("DPS") or file_names[i].startswith("DPC") and file_names[i].find("Address") == -1:
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
    for object_dictionary_i in rootD.xpath('//Object'):
        for attribute_dictionary_i in object_dictionary_i.findall('Attribute'):
            if attribute_dictionary_i.attrib.get('Name') == 'object address':
                mass.append(object_dictionary_i.attrib.get('Name') + '|' + attribute_dictionary_i.attrib.get('Value'))


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
#parsDict(dictionary_names[4], mass4)

print(mass0, mass1, mass2, mass3, mass4)

def replaceTOEId(attributeStr, mass0, mass1, mass2, mass3, mass4, count):
    replace = 0
    i=1
    while i < len(mass0) and replace == 0:
        temp = str(mass0[i].split('|')[0])
        tempRepl = str(mass0[i].split('|')[1])
        if attributeStr.find(temp) != -1:
            attributeStr = attributeStr.replace(temp, tempRepl)
            replace = 1
            break
        i+=1
    i=1
    while i < len(mass1) and replace == 0:
        temp = str(mass1[i].split('|')[0])
        tempRepl = str(mass1[i].split('|')[1])
        if attributeStr.find(temp) != -1:
            attributeStr = attributeStr.replace(temp, tempRepl)
            replace = 1
            break
        i+=1
    i=1
    while i < len(mass2) and replace == 0:
        temp = str(mass2[i].split('|')[0])
        tempRepl = str(mass2[i].split('|')[1])
        if attributeStr.find(temp) != -1:
            attributeStr = attributeStr.replace(temp, tempRepl)
            replace = 1
            break
        i+=1
    while i < len(mass3) and replace == 0:
        temp = str(mass3[i].split('|')[0])
        tempRepl = str(mass3[i].split('|')[1])
        if attributeStr.find(temp) != -1:
            attributeStr = attributeStr.replace(temp, tempRepl)
            replace = 1
            break
        i+=1
    return attributeStr
    

count = 0
for name in file_names:
    print(name)
    inputFile = et.parse(folderObjects + '\\' + name)
    root = inputFile.getroot()
    count=0
    tag=0
    
    for object_i in root.xpath('//Object'):
        for attribute_i in object_i.xpath('//TargetObjectExtId'):
            if type(attribute_i.text) == str and attribute_i.text.find("T104") != -1:
                #print(attribute_i.text)
                attribute_i.text = replaceTOEId(attribute_i.text, mass0, mass1, mass2, mass3, mass4, count)

    inputFile.write(folderNewObjects+ '\\' + name)


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

