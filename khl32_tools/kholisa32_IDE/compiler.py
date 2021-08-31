# This Python file uses the following encoding: utf-8
from typing import List, Set, Dict, Tuple, Optional

class Compiler:
    errors = []
    def __init__(self):
        pass

    def parse(line: str, nLine: int, PC: int, labels: Dict[str, int], errors: List[str]) -> str:
        if line == "":
            return None

        if line[0] == ';':
            return None

        elif line[0] == '"':
            return line

        elif line[0] == '.':
            if line[:5] == ".name":
                return line

            if line[:5] == ".icon":
                return line

            elif line[:4] == ".img":
                return line

            elif line[:6] == ".sound":
                return line

        elif line[0] == ('}' or '{'):
            return line

        """ Add to label """
        if not '"' in line and ":" in line:
            labels[line.upper()[:-1]] = PC
            return None

        command = line.split(" ")[0]
        line = line.replace(command, '')
        command = command.upper()
        if not '"' in line:
            line = line.replace(' ', '')
        else:
            line = line[1:]
        data = []

        if not command == "DEBUG" and "," in line:
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
                    errors.append("Error at line " + str(nLine))
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
            if len(data) < 1:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0]:
                    string = "0x04000000\n{}".format(data[0])
                else:
                    errors.append("Error at line " + str(nLine))

        elif command == "JMP":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0]:
                    string = "0x04000000\n{}".format(data[0])
                else:
                    errors.append("Error at line " + str(nLine))

        elif command == "CALL":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0]:
                    string = "0x05000000\n{}".format(data[0])
                else:
                    errors.append("Error at line " + str(nLine))


        elif command == "JNE":
            if len(data) < 3:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x07{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))

        elif command == "JE":
            if len(data) < 3:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x09{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))

        elif command == "MOV":
            if len(data) < 2:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                string = "0x0b{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine) + ": register not bewteen 0 and 255")
                        else:
                            val = -1
                            try:
                                val = int(data[1],10)
                            except:
                                try:
                                    val = int(data[1],16)
                                except:
                                    pass
                            if val >= 0 and val<=0xffffffff:
                                string = "0x0a{:02x}0000\n0x{:08x}".format(int(data[0][1:]), val)
                            else:
                                errors.append("Error at line " + str(nLine) + ":value is bigger than 32 bits")
                    else:
                        errors.append("Error at line " + str(nLine) + ": register not bewteen 0 and 255")
                else:
                    errors.append("Error at line " + str(nLine) + ": too few arguments given!")

        elif command == "RAND":
            if len(data) < 3:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R' and data[2][0].upper() == 'R':
                            if data[1][1:].isnumeric() and int(data[1][1:])<0xff and data[2][1:].isnumeric() and int(data[2][1:])<0xff:
                                string = "0x0d{:02x}{:02x}{:02x}".format(int(data[0][1:]), int(data[1][1:]), int(data[2][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))

        elif command == "ADD":
            if len(data) < 2:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                                string = "0x0f{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line" + str(nLine))
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
                                errors.append("Error at line" + str(nLine))
                    else:
                        errors.append("Error at line" + str(nLine))
                else:
                    errors.append("Error at line" + str(nLine))


        elif command == "SUB":
            if len(data) < 2:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                                string = "0x11{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "MUL":
            if len(data) < 2:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                                string = "0x13{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "DIV":
            if len(data) < 2:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                                string = "0x15{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))


        elif command == "MOD":
            if len(data) < 2:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if data[1][1:].isnumeric() and int(data[1][1:])<0xff:
                                string = "0x17{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))


        elif command == "LS":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
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
                            errors.append("Error at line " + str(nLine) + ": Value '" + val + "' not between 0 and 31")
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "RS":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
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
                            errors.append("Error at line " + str(nLine) + ": Value '" + str(val) + "' not between 0 and 31")
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))




        elif command == "LR":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
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
                            errors.append("Error at line " + str(nLine) + ": Value '" + val + "' not between 0 and 31")
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))

        elif command == "RR":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
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
                            errors.append("Error at line " + str(nLine) + ": Value '" + val + "' not between 0 and 31")
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))


        elif command == "INC":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        string = "0x1C{:02x}0000".format(int(data[0][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "DEC":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        string = "0x1D{:02x}0000".format(int(data[0][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))


        elif command == "DJNZ":
            if len(data) < 2:
                errors.append("Error at line" + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x1E{:02x}0000\n{}".format(int(data[0][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                        else:
                            errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))

        elif command == "DJE":
            if len(data) < 2:
                errors.append("Error at line" + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x1E{:02x}0000\n{}".format(int(data[0][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                        else:
                            errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "PUSH":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        string = "0x20{:02x}0000".format(int(data[0][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "POP":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        string = "0x21{:02x}0000".format(int(data[0][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))




        elif command == "AND":
            if len(data) < 2:
                errors.append("Error at line" + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                string = "0x23{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))




        elif command == "OR":
            if len(data) < 2:
                errors.append("Error at line" + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                string = "0x25{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "XOR":
            if len(data) < 2:
                errors.append("Error at line" + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                string = "0x27{:02x}{:02x}00".format(int(data[0][1:]), int(data[1][1:]))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))




        elif command == "COMP":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        string = "0x28{:02x}0000".format(int(data[0][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))


        elif command == "JLT":
            if len(data) < 3:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x31{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                    string = "0x30{:02x}0000\n0x{:08x}\n{}".format(int(data[0][1:]), val, data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))




        elif command == "JLE":
            if len(data) < 3:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x33{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                    string = "0x32{:02x}0000\n0x{:08x}\n{}".format(int(data[0][1:]), val, data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "JGT":
            if len(data) < 3:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x35{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                    string = "0x34{:02x}0000\n0x{:08x}\n{}".format(int(data[0][1:]), val, data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))







        elif command == "JGE":
            if len(data) < 3:
                errors.append("Error at line " + str(nLine))
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1].isnumeric() and int(data[0][1:])<0xff:
                        if data[1][0].upper() == 'R':
                            if int(data[1][1:])<0xff:
                                if data[2][0].isalpha():
                                    string = "0x37{:02x}{:02x}00\n{}".format(int(data[0][1:]), int(data[1][1:]), data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
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
                                    string = "0x36{:02x}0000\n0x{:08x}\n{}".format(int(data[0][1:]), val, data[2])
                                else:
                                    errors.append("Error at line " + str(nLine))
                            else:
                                errors.append("Error at line " + str(nLine))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))







        elif command == "DEBUG":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        string = "0xA2{:02x}0000".format(int(data[0][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
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
                    errors.append("Error at line " + str(nLine))



        elif command == "DISPBGCOLOR":
            if len(data) < 1:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff:
                        string = "0xA4{:02x}0000".format(int(data[0][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "DISPSTRING":
            data[1:] = [x.replace(' ', '') for x in data[1:]]
            if len(data) < 4:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0] == '"':
                    if data[1][0].upper() == 'R' and data[2][0].upper() == 'R' and data[3][0].upper() == 'R':
                        chars = [ord(c) for c in data[0][1:-1]]
                        string = "0xA5{:02x}{:02x}{:02x}\n0x{:02x}000000".format(int(len(chars)), int(data[1][1:]), int(data[2][1:]), int(data[3][1:]))
                        if len(chars)%4:
                            for k in range(0,4-len(chars)%4):
                                chars.append(0)
                        for n in range(0, int(len(chars)/4)):
                            string += "\n0x{:02x}{:02x}{:02x}{:02x}".format(chars[n*4+3],chars[n*4+2],chars[n*4+1],chars[n*4])
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))



        elif command == "DISPNUMBER":
            if len(data) < 4:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R' and data[1][0].upper() == 'R' and data[2][0].upper() == 'R' and data[3][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff and data[1][1:].isnumeric() and int(data[1][1:])<0xff and data[2][1:].isnumeric() and int(data[2][1:])<0xff and data[3][1:].isnumeric() and int(data[3][1:])<0xff:
                        string = "0xA6{:02x}{:02x}{:02x}\n0x{:02x}000000".format(int(data[0][1:]), int(data[1][1:]), int(data[2][1:]), int(data[3][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))





        elif command == "DRAWLINE":
            if len(data) < 5:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R' and data[1][0].upper() == 'R' and data[2][0].upper() == 'R' and data[3][0].upper() == 'R' and data[4][0].upper() == 'R':
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff and data[1][1:].isnumeric() and int(data[1][1:])<0xff and data[2][1:].isnumeric() and int(data[2][1:])<0xff and data[3][1:].isnumeric() and int(data[3][1:])<0xff and data[4][1:].isnumeric() and int(data[4][1:])<0xff:
                        string = "0xB0{:02x}{:02x}{:02x}\n0x{:02x}{:02x}0000".format(int(data[0][1:]), int(data[1][1:]), int(data[2][1:]), int(data[3][1:]), int(data[4][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))




        elif command == "DRAWRECT":
            if len(data) < 5:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R' and data[1][0].upper() == 'R' and data[2][0].upper() and data[3][0].upper() and data[4][0].upper():
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff and data[1][1:].isnumeric() and int(data[1][1:])<0xff and data[2][1:].isnumeric() and int(data[2][1:])<0xff and data[3][1:].isnumeric() and int(data[3][1:])<0xff and data[4][1:].isnumeric() and int(data[4][1:])<0xff:
                        string = "0xB1{:02x}{:02x}{:02x}\n0x{:02x}{:02x}0000".format(int(data[0][1:]), int(data[1][1:]), int(data[2][1:]), int(data[3][1:]), int(data[4][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))





        elif command == "DRAWCIRCLE":
            if len(data) < 4:
                errors.append("Error at line " + str(nLine) + ": too few arguments given!")
            else:
                if data[0][0].upper() == 'R' and data[1][0].upper() == 'R' and data[2][0].upper() and data[3][0].upper():
                    if data[0][1:].isnumeric() and int(data[0][1:])<0xff and data[1][1:].isnumeric() and int(data[1][1:])<0xff and data[2][1:].isnumeric() and int(data[2][1:])<0xff and data[3][1:].isnumeric() and int(data[3][1:])<0xff:
                        string = "0xB2{:02x}{:02x}{:02x}\n0x{:02x}000000".format(int(data[0][1:]), int(data[1][1:]), int(data[2][1:]), int(data[3][1:]))
                    else:
                        errors.append("Error at line " + str(nLine))
                else:
                    errors.append("Error at line " + str(nLine))

        else:
            errors.append("Error at line " + str(nLine) + ": " + "command " + "'" + command + "' does not exist!")


        return string



    def compileTemp(strin: str) -> Tuple[str, Dict[str, int]]:
        PC = 0
        labels = {}
        strout = ""
        for index, line in enumerate(strin.split("\n")):
            output = Compiler.parse(line.strip(), index+1, PC, labels, Compiler.errors)
            if output:
                if output[:2] == "0x":
                    PC += output.count("\n")+1
                strout += output + "\n"

        return strout, labels

    def replaceLabels(strin: str, labels: Dict[str, int]) -> str:
        """
        for line in lout:
            if line[0].isalpha():
                labels[line[:line.find(":")]] = line[line.find(":"):]
        """
        strout = ""
        for line in strin.split("\n"):
            line = line.strip()
            if line and line[0].isalpha():
                strout += "0x{:08x}\n".format(labels[line])
            else:
                strout += line + "\n"
        return strout

    def compile(strin: str) -> str:
        tmpGameText, labels = Compiler.compileTemp(strin)
        game = Compiler.replaceLabels(tmpGameText, labels)
        return game
