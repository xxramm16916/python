import codecs
import xml.etree.ElementTree as ET

#--------------------------interface------------------------------------------
outputFile = codecs.open(r"C:\Users\User\Desktop\дб1\kc_xml\моя-41\aaa.csv", "w", 'utf-8')
inputFile = ET.parse(r'C:\Users\User\Desktop\дб1\kc_xml\моя-41\iec104_serv.xml')
objectCode = 'MD21PD01PS99'
#-----------------------------------------------------------------------------

root = inputFile.getroot()

def writeToFile(data, typeD, flag):
        writeLine = data.strip()
        '''
        if typeD == 0:
            writeLine = writeLine.replace("[", "")
            writeLine = writeLine.replace("]", "")
        if typeD == 1 and data != '':
            writeLine = writeLine.replace("Name=", "")
        if typeD == 2 and data != '':
            writeLine = writeLine.replace("MODULE=", "")
        if typeD == 3 and data != '':
            writeLine = writeLine.replace("IEC_Adr=", "")
        '''
        outputFile.write(writeLine)
        outputFile.write(';')
        if flag == 1:
            outputFile.write(objectCode)
            outputFile.write(';')
            outputFile.write('\n')


count=0
for POINT in root.iter('POINT'):
    name = POINT.get('NAME')
    address = POINT.get('ADDRESS')
    asduType = POINT.get('ASDU_TYPE')
    if asduType == '30' or asduType == '36':
        writeToFile(name, 1, 0)
        writeToFile(address, 2, 0)
        writeToFile(asduType, 3, 1)
        count+=1
print (count)

outputFile.close()




