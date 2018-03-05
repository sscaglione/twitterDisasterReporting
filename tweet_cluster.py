import json
#Read in tweets as json, create bag of words from sanitized text body
tweets = {}

#Remove urls, @'s, "RT", etc. Remove numbers, symbols, and make lowercase 
def bag_of_words(line):
	words = []
	line = line.split()
	for word in line:
		if not word.isalpha():
			if "@" not in word and "http" not in word:
				l_word = [x for x in word if x.isalpha()]
				word = "".join(l_word)
				if word != "":
					words.append(word.lower())
		else:
			if word != "RT" and word != "rt":
				words.append(word.lower())
	return words

with open("sandy.json") as f:
	for line in f:
		try:
			t = json.loads(line)
			print(t['text'])
			if t['text']:
				words = t['text']
			tweets[t["id"]] = bag_of_words(words)
		except json.decoder.JSONDecodeError as e:
			print("no")
	print(tweets)