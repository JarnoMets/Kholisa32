import sys
import math

def parse(line, nLine, PC, labels):

    if line[0] == '.':
        if line[:5] == ".name":
            pass
        
        elif line[:4] == ".img":
            pass
    
    if line == "":
        return None
    
    """ Add to label """
    if not '"' in line and ":" in line:
        labels[line.upper()[:-1]] = PC
        #print("PC " + line + str(PC))
        return None
    
    command = line.split(" ")[0].upper()
    line = line.replace(command, '')
    if not '"' in line:
        line = line.replace(' ', '')
    else:
        line = line[1:]
    data = []
    
    if not '"' in line and "," in line:
        data = line.upper().split(",")
    elif '"' in line:
        data.append(line)
    elif line:
        data.append(line.upper())

    
    string = ""

    if command == '':
        pass
        
    elif command == "NOP":
        string = "0x00000000"

    elif command == "STOP":
        if len(data):
            if data[0].isnumeric() and int(data[0])<0xff:
                string = "0x00{:02x}0000".format((int(data[0])))
            else:
                exit("Error at line " + str(nLine))
        else:
            string = "0x00010000"

    elif command == "CLEAR":
        string = "0x01000000"

    elif command == "RET":
        string = "0x02000000"

    elif command == "SJMP":
        """
        Legacy
        Will compile to (long) jump (JMP)
        """
        if data[0]:
            string = "0x04000000\n:{}".format(data[0])
        else:
            exit("Error at line " + str(nLine))

    elif command == "JMP":
        if data[0]:
            string = "0x04000000\n{}".format(data[0])
        else:
            exit("Error at line " + str(nLine))

    elif command == "CALL":
        if data[0]:
            string = "0x05000000\n:{}".format(data[0])
        else:
            exit("Error at line " + str(nLine))
    
    
    elif command == "JNE":
        if len(data) < 3:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        if data[2][0].isalpha():
                            string = "0x07{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                        else:
                            exit("Error at line" + str(nLine))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff:
                        if data[2][0].isalpha():
                            string = "0x06{:02x}0000\n0x{:08x}\n{}".format(int(data[0][1:]), val, data[2])
                        else:
                            exit("Error at line" + str(nLine))
                    else:
                        exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))

    elif command == "JE":
        if len(data) < 3:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        if data[2][0].isalpha():
                            string = "0x09{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                        else:
                            exit("Error at line" + str(nLine))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff:
                        if data[2][0].isalpha():
                            string = "0x08{:02x}0000\n0x{:08x}\n{}".format(int(data[0][1:]), val, data[2])
                        else:
                            exit("Error at line" + str(nLine))
                    else:
                        exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))

    elif command == "MOV":
        if len(data) < 2:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        string = "0x0b{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff:
                        string = "0x0a{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))

    elif command == "RAND":
        if len(data) < 3:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R' and data[2][0].upper() == 'R':
                    if data[1][1:].isnumeric() and int(data[1][1:])<0xff and data[2][1:].isnumeric() and int(data[2][1:])<0xff:
                        string = "0x0d{:02x}{:02x}{:02x}".format(int(data[0][1:]), int(data[1][1:]), int(data[2][1:]))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    val1 = -1
                    val2 = -1
                    try:
                        val1 = int(data[1],10)
                    except:
                        try:
                            val1 = int(data[1],16)
                        except:
                            pass

                    try:
                        val2 = int(data[2],10)
                    except:
                        try:
                            val2 = int(data[2],16)
                        except:
                            pass
                    if val1 >= 0 and val1<0xffffffff and val2 >= 0 and val2<0xffffffff:
                        string = "0x0c{:02x}0000\n0x{:08x}\n0x{:08x}".format(int(data[0][1:]), val1, val2)
                    else:
                        exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))

    elif command == "ADD":
        if len(data) < 2:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                        string = "0x0f{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line " + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff and val >= 0 and val<0xffffffff:
                        string = "0x0e{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line " + str(nLine))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))


    elif command == "SUB":
        if len(data) < 2:
            exit("Error at line " + str(nLine) + ": too few arguments given!")
        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                        string = "0x11{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line " + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff and val >= 0 and val<0xffffffff:
                        string = "0x10{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line " + str(nLine))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))



    elif command == "MUL":
        if len(data) < 2:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                        string = "0x13{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line " + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass

                    if val >= 0 and val<0xffffffff and val >= 0 and val<0xffffffff:
                        string = "0x12{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line " + str(nLine))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))



    elif command == "DIV":
        if len(data) < 2:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                        string = "0x15{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line " + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass

                    if val >= 0 and val<0xffffffff and val >= 0 and val<0xffffffff:
                        string = "0x14{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line " + str(nLine))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))


    elif command == "MOD":
        if len(data) < 2:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                        string = "0x17{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line " + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass

                    if val >= 0 and val<0xffffffff and val >= 0 and val<0xffffffff:
                        string = "0x16{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line " + str(nLine))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))


    elif command == "LS":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                val = -1
                try:
                    val = int(data[1],10)
                except:
                    try:
                        val = int(data[1],16)
                    except:
                        pass

                if val >= 0 and val<32 and val >= 0 and val<32:
                    string = "0x18{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                else:
                    exit("Error at line " + str(nLine) + ": Value '" + val + "' not between 0 and 31")
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))



    elif command == "RS":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                val = -1
                try:
                    val = int(data[1],10)
                except:
                    try:
                        val = int(data[1],16)
                    except:
                        pass

                if val >= 0 and val<32 and val >= 0 and val<32:
                    string = "0x19{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                else:
                    exit("Error at line " + str(nLine) + ": Value '" + val + "' not between 0 and 31")
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))




    elif command == "LR":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                val = -1
                try:
                    val = int(data[1],10)
                except:
                    try:
                        val = int(data[1],16)
                    except:
                        pass

                if val >= 0 and val<32 and val >= 0 and val<32:
                    string = "0x1A{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                else:
                    exit("Error at line " + str(nLine) + ": Value '" + val + "' not between 0 and 31")
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))

    elif command == "RR":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                val = -1
                try:
                    val = int(data[1],10)
                except:
                    try:
                        val = int(data[1],16)
                    except:
                        pass

                if val >= 0 and val<32 and val >= 0 and val<32:
                    string = "0x1B{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                else:
                    exit("Error at line " + str(nLine) + ": Value '" + val + "' not between 0 and 31")
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))


    elif command == "INC":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                string = "0x1C{:02x}0000".format(int(data[0][1:]))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))



    elif command == "DEC":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                string = "0x1D{:02x}0000".format(int(data[0][1:]))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))


    elif command == "DJNZ":
        if len(data) < 2:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        if data[2][0].isalpha():
                            string = "0x1E{:02x}0000\n{}".format(int(data[0][1:]), data[2])
                        else:
                            exit("Error at line" + str(nLine))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))

    elif command == "DJE":
        if len(data) < 2:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        if data[2][0].isalpha():
                            string = "0x1E{:02x}0000\n{}".format(int(data[0][1:]), data[2])
                        else:
                            exit("Error at line" + str(nLine))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))



    elif command == "PUSH":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                string = "0x20{:02x}0000".format(int(data[0][1:]))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))



    elif command == "POP":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                string = "0x21{:02x}0000".format(int(data[0][1:]))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))




    elif command == "AND":
        if len(data) < 2:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        string = "0x23{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff:
                        string = "0x22{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))




    elif command == "OR":
        if len(data) < 2:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        string = "0x25{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff:
                        string = "0x24{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))



    elif command == "XOR":
        if len(data) < 2:
            exit("Error at line" + str(nLine))

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                if data[1][0].upper() == 'R':
                    if int(data[1][1:])<0xff:
                        string = "0x27{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                    else:
                        exit("Error at line" + str(nLine))
                else:
                    val = -1
                    try:
                        val = int(data[1],10)
                    except:
                        try:
                            val = int(data[1],16)
                        except:
                            pass
                    if val >= 0 and val<0xffffffff:
                        string = "0x26{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                    else:
                        exit("Error at line" + str(nLine))
            else:
                exit("Error at line" + str(nLine))
        else:
            exit("Error at line" + str(nLine))




    elif command == "COMP":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                string = "0x28{:02x}0000".format(int(data[0][1:]))
            else:
                exit("Error at line " + str(nLine))
        else:
            exit("Error at line " + str(nLine))





    elif command == "DEBUG":
        if len(data) < 1:
            exit("Error at line " + str(nLine) + ": too few arguments given!")

        if data[0][0].upper() == 'R':
            if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                string = "0xA2{:02x}0000".format(int(data[0][1:]))
            else:
                exit("Error at line " + str(nLine))
        elif data[0][0] == '"':
            chars = [ord(c) for c in data[0][1:-1]]
            string = "0xA3{:02x}0000".format(int(len(chars)))
            if len(chars)%4:
                for k in range(0,4-len(chars)%4):
                    chars.append(0)
            for n in range(0, int(len(chars)/4)):
                string += "\n0x{:02x}{:02x}{:02x}{:02x}".format(chars[n*4+3],chars[n*4+2],chars[n*4+1],chars[n*4])
            
            """ TBI """
        else:
            exit("Error at line " + str(nLine))
    else:
        exit("Error at line" + str(nLine) + ": " + "command " + "'" + command + "' does not exist")

    return string


def compileTemp(fin, fout, lout):
    PC = 0
    labels = {}
    for index, line in enumerate(fin):
        #print(parse(line.rstrip(), index) + "\n")
        #output = parse(unicode(line.rstrip(), "utf-8"), index+1, PC, labels)
        output = parse(line.rstrip(), index+1, PC, labels)
        if output:
            PC += output.count("\n")+1
            fout.write(output + "\n")


    if len(labels):
        lout.write("#labels { \n")
        for _, (label, PC) in enumerate(labels.items()):
            lout.write(label + ':' + str(PC) + "\n")
            
        lout.write("} #endLables")
    return labels
    
def replaceLabels(ftmp, fout, labels):
    """
    for line in lout:
        if line[0].isalpha():
            labels[line[:line.find(":")]] = line[line.find(":"):]
    """
    for line in ftmp:
        line = line.strip()
        if line[0].isalpha():
            fout.write("0x{:08x}\n".format(labels[line]))
        else:
            fout.write(line + "\n")
    
def main(argc, argv):
    if argc < 2:
        print("No input file given!")
        return -1

    try:
        ftmp = open("tmp.txt", "w+")
    except:
        return -2
        
    try:
        fin = open(argv[1], "r")
    except:
        print('Could not find "' + argv[1] + '"')
        return -2

    if argc > 2:
        try:
            fout = open(argv[2], "w+")
        except:
            print('Could not open "' + argv[2] + '"')
            return -2
    else:
        fout = open("output.txt","w+")

    try:
        lout = open("labels.txt", "w+")
    except:
        print('Could not open labels \n')
        return -3
   
    labels = compileTemp(fin, ftmp, lout)
    ftmp.close()
    try:
        ftmp = open("tmp.txt", "r")
    except:
        return -2
    replaceLabels(ftmp, fout, labels)

    fin.close()
    fout.close()
    lout.close()

    return 0






if __name__ == "__main__":
    print("Finished program with error code " + str(main(len(sys.argv), sys.argv)))
