import codecs
import re
import unicodedata as ud

#--------------------------interface------------------------------------------
outputFile = codecs.open(r"C:\Users\User\Desktop\работа\ДВ1\ЭКОМ конфигурации\НПС-24\bbb.csv", "w", 'utf-8')
inputFile = codecs.open(r'C:\Users\User\Desktop\работа\ДВ1\ЭКОМ конфигурации\НПС-24\НПС №24.INI', 'r', 'cp866')
objectCode = 'MD21PD01PS09'
#-----------------------------------------------------------------------------

def writeline(channel, name, module, iec_adr, mask, str_mask, number, magnitude):
        magnitude = magnitude.lower()
        outputFile.write(channel)
        outputFile.write(';')

        outputFile.write(name)
        outputFile.write(';')

        outputFile.write(module)
        outputFile.write(';')

        if str_mask == '2' and iec_adr != '-1':
                iec_adr = str(int(iec_adr) + 1)
        if str_mask == '4' and iec_adr != '-1':
                iec_adr = str(int(iec_adr) + 2)
        if str_mask == '8' and iec_adr != '-1':
                iec_adr = str(int(iec_adr) + 3)
        if str_mask == '16' and iec_adr != '-1':
                iec_adr = str(int(iec_adr) + 4)
        if str_mask == '32' and iec_adr != '-1':
                iec_adr = str(int(iec_adr) + 5)
        if str_mask == '64' and iec_adr != '-1':
                iec_adr = str(int(iec_adr) + 6)
        if str_mask == '128' and iec_adr != '-1':
                iec_adr = str(int(iec_adr) + 7)
                
        outputFile.write(iec_adr)
        outputFile.write(';')
        outputFile.write(objectCode)
        outputFile.write(';')
        outputFile.write(';;;;')
        #outputFile.write(str_mask) #отладка для постфиксов
        #outputFile.write(' --- ')
        #outputFile.write(number)
        #outputFile.write(' --- ')
        #outputFile.write(magnitude)
        #print(type(magnitude))
        
        if str_mask == '64': #накопительный итог
            #print(magnitude, '      ', 'квтч'.decode('cp1251'))
            if number == '1' and magnitude == 'квтч'.decode('cp1251'):
                outputFile.write('APd')
                outputFile.write(';')
            if number == '2' and magnitude == 'квтч'.decode('cp1251'):
                outputFile.write('BAPd')
                outputFile.write(';')
            if number == '3' and magnitude == 'кврч'.decode('cp1251'):
                outputFile.write('RPEd')
                outputFile.write(';')
            if number == '4' and magnitude == 'кврч'.decode('cp1251'):
                outputFile.write('BRPEd')
                outputFile.write(';')
        if str_mask == '2': #За короткий
            if number == '1' and magnitude == 'квт'.decode('cp1251'):
                outputFile.write('PAAV5m')
                outputFile.write(';')
            if number == '2' and magnitude == 'квт'.decode('cp1251'):
                outputFile.write('BPAAV5m')
                outputFile.write(';')
            if number == '3' and magnitude == 'квар'.decode('cp1251'):
                outputFile.write('PRAVE5m')
                outputFile.write(';')
            if number == '4' and magnitude == 'квар'.decode('cp1251'):
                outputFile.write('BPRAVE5m')
                outputFile.write(';')
        if str_mask == '4': #За сновной
            if number == '1' and magnitude == 'квтч'.decode('cp1251'):
                outputFile.write('AP30m')
                outputFile.write(';')
            if number == '2' and magnitude == 'квтч'.decode('cp1251'):
                outputFile.write('BAP30m')
                outputFile.write(';')
            if number == '3' and magnitude == 'кврч'.decode('cp1251'):
                outputFile.write('RPE30m')
                outputFile.write(';')
            if number == '4' and magnitude == 'кврч'.decode('cp1251'):
                outputFile.write('BRPE30m')
                outputFile.write(';')
            if number == '1' and magnitude == 'квт'.decode('cp1251'):
                outputFile.write('PAAV30m')
                outputFile.write(';')
            if number == '2' and magnitude == 'квт'.decode('cp1251'):
                outputFile.write('BPAAV30m')
                outputFile.write(';')
            if number == '3' and magnitude == 'квар'.decode('cp1251'):
                outputFile.write('PRAVE30m')
                outputFile.write(';')
            if number == '4' and magnitude == 'квар'.decode('cp1251'):
                outputFile.write('BPRAVE30m')
                outputFile.write(';')
                
        outputFile.write('\n')
        

def writeToFile_v3(channel, name, module, iec_adr, mask, number_f, magnitude):
        channel = channel.strip()
        name = name.strip()
        module = module.strip()
        iec_adr = iec_adr.strip()
        mask = mask.strip()
        number_f = number_f.strip()
        magnitude = magnitude.strip()
         
        channel = channel.replace("[", "")
        channel = channel.replace("]", "")
        name = name.replace("Name=", "")
        module = module.replace("MODULE=", "")
        iec_adr = iec_adr.replace("IEC_Adr=", "")
        mask = mask.replace("IEC_Mask=", "")
        number_f = number_f.replace("NUMBER=", "")
        magnitude = magnitude.replace("Units=", "")
        
        temp_mask = int(mask)
        for number in reversed(range(8)):
            difference = temp_mask - pow(2, number)
            if difference > 0 and not iec_adr == '-1':
                temp_mask = difference
                writeline(channel, name, module, iec_adr, mask, str(pow(2, number)), number_f, magnitude);
                #outputFile.write(str(pow(2, number)))
                #outputFile.write(';     ')
            if difference == 0 or iec_adr == '-1':
                temp_mask = difference
                writeline(channel, name, module, iec_adr, mask, str(pow(2, number)), number_f, magnitude);
                break
        #outputFile.write('\n')


        
line = inputFile.readline()
while line:
    channel = ''
    name = ''
    module = ''
    iec_adr = ''
    mask = ''
    number = ''
    magnitude = ''
    if re.search('\[[BEGS]{,1}\d*\]', line):
        #print (line)
        channel = line
        line = inputFile.readline()
        nameFind = 0
        moduleFind = 0
        addrFind = 0
        maskFind = 0
        numberFind = 0
        magnitudeFind = 0
        while line and not re.search('\[\w*\]', line):
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
            line = inputFile.readline()
        #print(channel, name, module, iec_adr, mask, number, magnitude)
        writeToFile_v3(channel, name, module, iec_adr, mask, number, magnitude)
    if not re.search('\[[BEGS]{,1}\d*\]', line):
        line = inputFile.readline()
inputFile.close()
outputFile.close()
