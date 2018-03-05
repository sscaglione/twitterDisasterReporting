import json

#Fix text file json structure
with open("sandy_sample.txt") as f:
	with open("sandy.json", "w+") as out:
		for line in f:
			line = line.rstrip().replace("None", "\"null\"")
			line_fix = []
			for c in line:
				line_fix.append(c)
			i = 1
			#print(line_fix)
			while i < len(line_fix) - 1:
				if line_fix[i] == "\'" and line_fix[i-1] == "u":
					#print("HERE")
					line_fix[i-1] = "0"
					while line_fix[i] != "," and line_fix[i] != "}":
						line_fix[i] = ""
						i += 1
				if line_fix[i] == "\'" and (line_fix[i-1] == " " or line_fix[i-1] == "{" or line_fix[i+1] == "," or line_fix[i+1] == ":" or line_fix[i+1] == "}"):
					line_fix[i] = "\""
				i += 1
			line = "".join(line_fix)
			out.write(line + "\n")
