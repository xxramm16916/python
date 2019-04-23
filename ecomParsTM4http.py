import codecs
import re
import unicodedata as ud

#--------------------------interface------------------------------------------
outputFile = codecs.open(r"C:\Users\User\Desktop\работа\ДВ1\ЭКОМ конфигурации\НПС-24\bbb.csv", "w", 'utf-8')
inputStr = r'C:\Users\User\Desktop\работа\ДВ1\ЭКОМ конфигурации\НПС-24\НПС №24.INI'
objectCode = 'MD21PD01PS02'
#-----------------------------------------------------------------------------


inputFile = codecs.open(inputStr, 'r', 'cp866')
inputModules = codecs.open(inputStr, 'r', 'cp866')


def writeline(channel, name, module, iec_adr, magnitude, postfix, number):
        magnitude = magnitude.lower()
        outputFile.write(channel)
        outputFile.write(';')

        outputFile.write(name)
        outputFile.write(';')

        outputFile.write(module)
        outputFile.write(';')

        outputFile.write(iec_adr)
        outputFile.write(';')
        outputFile.write(objectCode)
        outputFile.write(';')
        outputFile.write(';;;;')
        outputFile.write(postfix)
        outputFile.write(';')

        #outputFile.write('                       ;')
        #outputFile.write(number)


        outputFile.write('\n')
        

def writeToFile_v3(channel, name, module, iec_adr, mask, number, magnitude, coeff, listModules):
        channel = channel.strip()
        name = name.strip()
        module = module.strip()
        iec_adr = iec_adr.strip()
        mask = mask.strip()
        number = number.strip()
        magnitude = magnitude.strip()
        coeff = coeff.strip()
         
        channel = channel.replace("[", "")
        channel = channel.replace("]", "")
        name = name.replace("Name=", "")
        module = module.replace("MODULE=", "")
        iec_adr = iec_adr.replace("IEC_Adr=", "")
        mask = mask.replace("IEC_Mask=", "")
        number = number.replace("NUMBER=", "")
        magnitude = magnitude.replace("Units=", "")
        coeff = coeff.replace("COEFF=", "")

        strCompare = module + '|' + coeff
        #print(listModules)
        if strCompare in listModules:
            if number == '1':
                writeline(channel, name, module, iec_adr, magnitude, 'PAAV30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'PAAV5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'APd', number)
                writeline(channel, name, module, iec_adr, magnitude, 'AP30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'AP5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'PAAVd', number)
            if number == '2':
                writeline(channel, name, module, iec_adr, magnitude, 'BPAAV30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BPAAV5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BAPd', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BAP30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BAP5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BPAAVd', number)
            if number == '3':
                writeline(channel, name, module, iec_adr, magnitude, 'PRAVE30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'PRAVE5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'RPEd', number)
                writeline(channel, name, module, iec_adr, magnitude, 'RPE30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'RPE5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'PRAVEd', number)
            if number == '4':
                writeline(channel, name, module, iec_adr, magnitude, 'BPRAVE30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BPRAVE5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BRPEd', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BRPE30m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BRPE5m', number)
                writeline(channel, name, module, iec_adr, magnitude, 'BPRAVEd', number)
            #print(channel, strCompare)
            


def parsModule(module, ti, tu):
    module = module.strip()
    ti = ti.strip()
    tu = tu.strip()

    module = module.replace("[Module ", "")
    module = module.replace("]", "")
    ti = ti.replace("T_I=", "")
    tu = tu.replace("T_U=", "")
    
    if ti == '':
        ti = 1
    else:
        ti = eval(ti)
        
    if tu == '':
        tu = 1
    else:
        tu = eval(tu)

    return module + '|' + str(ti*tu)
        

listModules = []
line = inputModules.readline()
i = 0
while line:
    module = ''
    ti = ''
    tu = ''
    if re.search('\[Module \d*\]', line):
        module = line
        line = inputFile.readline()
        #print(line)
        while line and not re.search('\[\w*|\w* \d*\]', line):
            if 'T_I=' in line:
                ti = line
                #print(line)
            if 'T_U=' in line:
                tu = line
                #print(line)
            line = inputModules.readline()
        if module != '[Module 1]\r\n':
            listModules.append(parsModule(module, ti, tu))
    if not re.search('\[Module \d*\]', line):
        line = inputModules.readline()
inputModules.close()
#print (listModules)
#print (len(listModules))
#if re.search('\[\w*|\w* \d*\]', '[B140]'):
#    print('yes')

line = inputFile.readline()
while line:
    channel = ''
    name = ''
    module = ''
    iec_adr = ''
    mask = ''
    number = ''
    magnitude = ''
    coeff = ''
    if re.search('\[B{,1}\d*\]', line):
        #print (line)
        channel = line
        line = inputFile.readline()
        nameFind = 0
        moduleFind = 0
        addrFind = 0
        maskFind = 0
        numberFind = 0
        magnitudeFind = 0
        coeffFind = 0
        while line and not re.search('\[\w*|\w* \d*\]', line):
                #Wizard_Units=
            if 'Units=' in line and magnitudeFind == 0:
                magnitude = line
                magnitudeFind = 1
                #print (line)
            if 'Name=' in line and nameFind == 0:
                name = line
                nameFind = 1
                #print (line)
            if 'MODULE='in line and moduleFind == 0:
                module = line
                moduleFind = 1
                #print (line)
            if 'IEC_Adr=' in line and addrFind == 0:
                iec_adr = line
                addrFind = 1
                #print (line)
            if 'IEC_Mask=' in line and maskFind == 0:
                mask = line
                maskFind = 1
            if 'NUMBER=' in line and numberFind == 0:
                number = line
                numberFind = 1
                #print (line)
            if 'COEFF=' in line and coeffFind == 0:
                coeff = line
                coeffFind = 1
                #print (line)
            line = inputFile.readline()
        #print(channel, name, module, iec_adr, mask, number, magnitude)
        writeToFile_v3(channel, name, module, iec_adr, mask, number, magnitude, coeff, listModules)
    if not re.search('\[B{,1}\d*\]', line):
        line = inputFile.readline()
inputFile.close()
outputFile.close()
