import sys

def parse(line, nLine, dp, labels):
	""" Add to label """
	if ":" in line:
		labels[line] = dp
		print(dp)
		return None

	command = line.split(" ")[0].upper()
	line = line.replace(command, '').replace(' ', '')
	data = []

	if "," in line:
		data = line.upper().split(",")
	elif line:
		data.append(line.upper())

	if command == "NOP":
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
		dp += 1

	elif command == "RET":
		string = "0x02000000"
		dp += 1
		
	elif command == "SJMP":
		"""
		Legacy
		Will compile to (long) jump (JMP)
		"""
		if data[0]:
			string = "0x04000000\n:{}".format(data[0])
			dp += 2
		else:
			exit("Error at line " + str(nLine))

	elif command == "JMP":
		if data[0]:
			string = "0x04000000\n:{}".format(data[0])
		else:
			exit("Error at line " + str(nLine))
		
	elif command == "CALL":
		if data[0]:
			string = "0x05000000\n:{}".format(data[0])
		else:
			exit("Error at line " + str(nLine))
		
	elif command == "JNE":
		pass
		
	elif command == "JE":
		pass

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
					val = int(data[0],10)
				except:
					try:
						val = int(data[0],16)
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
					val = int(data[0],10)
				except:
					try:
						val = int(data[0],16)
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
					val = int(data[0],10)
				except:
					try:
						val = int(data[0],16)
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
					val = int(data[0],10)
				except:
					try:
						val = int(data[0],16)
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




	else:
		exit("Error at line" + str(nLine) + ": " + "command " + "'" + command + "' does not exist")
		
	return string
                
    
def compileTemp(fin, fout, lout):
	dp = 0; 
	labels = {}
	for index, line in enumerate(fin):
		#print(parse(line.rstrip(), index) + "\n")
		output = parse(unicode(line.rstrip(), "utf-8"), index+1, dp, labels)
		if output:
			dp += output.count("\n")+1
			fout.write(output + "\n")
	fout.close()
	if len(labels):
		lout.write("#labels { \n")
		for _, (label, dp) in enumerate(labels.items()):
			lout.write(label + ":" + str(dp) + "\n")
		lout.write("} #endLables")
	lout.close()

def main(argc, argv):
	if argc < 2:
		print("No input file given!")
		return -1

	try:
		fin = open(argv[1], "r")
	except:
		print('Could not find "' + argv[1] + '"')
		return -2
		
	if argc > 2:
		try:
			fout = open(argv[2], "w")
		except:
			print('Could not open "' + argv[2] + '"')
			return -2
	else:
		fout = open("tmp.txt","w+")
		
	try:
		lout = open("labels.txt", "w")
	except:
		print('Could not open labels \n')
		return -3

	compileTemp(fin, fout, lout)
	return 0
    
    
 
    
    

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
