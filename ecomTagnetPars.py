import os
import codecs
import lxml.etree as et
strPath = r'C:\Users\User\Desktop\zzz\ЦРС и БПО (10_221_164_11) MD14PD04PS22'
inputStrConfig = strPath + r'\config.xml' #config.xml
inputStrTagList = strPath + r'\tag-list' #tag-list
inputStrTreeConfig = strPath + r'\tree-config.xml' #tree-config.xml
outputStrFile = strPath + r'\10_221_164_11.csv' #output.csv

def get_last_digits(num, last_digits_count):
    return abs(num) % (10**last_digits_count)

inputFileConfig = et.parse(inputStrConfig)
root = inputFileConfig.getroot()
countTags=0

config = []
count = 0
for object_i in root.xpath('//ParametersGroup'):
    for attribute_i in object_i.findall('Parameter'):
        config.append(attribute_i.attrib.get('valueTag') + '|' + 'B'+str(get_last_digits(int(attribute_i.attrib.get('address')), 3)))
        count += 1

print(str(len(config)) + '|' + str(count))

inputTagList = open(inputStrTagList, 'r')
countLine = 0
tagList = []

for line in inputTagList:
    tagList.append(line.replace('=', '|'))
    countLine += 1

print(str(len(tagList)) + '|' + str(countLine))
inputTagList.close()

inputTreeConfig = et.parse(inputStrTreeConfig)
rootTree = inputTreeConfig.getroot()
countTags=0

configDescription = []
countDescription = 0
for object_i in rootTree.xpath('//Tag'):
    configDescription.append(object_i.attrib.get('name') + '|' + object_i.attrib.get('description'))
    countDescription += 1

print(str(len(configDescription)) + '|' + str(countDescription))

outputFile = codecs.open(outputStrFile, "w", 'utf-8')

for tag in tagList:
    des = ''
    ch = ''
    desFind = 0
    chFind = 0
    for description in configDescription:
        if tag.split('|')[0] == description.split('|')[0]:
            des = description.split('|')[1]
            desFind = 1
            break
    for channell in config:
        if tag.split('|')[0] == channell.split('|')[0]:
            ch = channell.split('|')[1]
            chFind = 1
            break
    if tag.strip().split('|')[0].find('.PAAV') != -1:
        flag = 'true'
    else:
        flag = 'false'
    if ch == '':
        if tag.strip().split('|')[0].find('.PAAV') != -1:
            outputFile.write(tag.strip().split('|')[0] + ';'+ des + ';' + tag.strip().split('|')[1][0] + ';' + tag.strip().split('|')[0].replace('.PAAV', '.AP') + ';' + 'true' + ';' + flag + ';' + '0' + ';\n')
        elif tag.strip().split('|')[0].find('.BPAAV') != -1:
            outputFile.write(tag.strip().split('|')[0] + ';'+ des + ';' + tag.strip().split('|')[1][0] + ';' + tag.strip().split('|')[0].replace('.BPAAV', '.BAP') + ';' + 'true' + ';' + flag + ';' + '0' + ';\n')
        elif tag.strip().split('|')[0].find('.PRAVE') != -1:
            outputFile.write(tag.strip().split('|')[0] + ';'+ des + ';' + tag.strip().split('|')[1][0] + ';' + tag.strip().split('|')[0].replace('.PRAVE', '.RPE') + ';' + 'true' + ';' + flag + ';' + '0' + ';\n')
        elif tag.strip().split('|')[0].find('.BPRAVE') != -1:
            outputFile.write(tag.strip().split('|')[0] + ';'+ des + ';' + tag.strip().split('|')[1][0] + ';' + tag.strip().split('|')[0].replace('.BPRAVE', '.BRPE') + ';' + 'true' + ';' + flag + ';' + '0' + ';\n')
        else:
            print(" ERROR. Tag ND!!" + tag.strip().split('|')[0])
    else:
        outputFile.write(tag.strip().split('|')[0] + ';'+ des + ';' + tag.strip().split('|')[1][0] + ';' + ch + ';' + 'true' + ';' + flag + ';' + '0' + ';\n')

outputFile.close()
