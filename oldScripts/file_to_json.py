import json
import sys

#Fix json structure for entire text file
with open(sys.argv[1]) as f:
	name = sys.argv[1].split(".")[0] + ".json"
	with open(name, "w+") as out:
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
