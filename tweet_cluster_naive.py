import json
import numpy as np
from sklearn import cluster
#Read in tweets as json, create bag of words from sanitized text body
tweets = {}

keywords_a = set(("flood", "flooding", "flooded", "overflow", "flow", "stream", "river", "overflowed", "soaked", "level"))
keywords_b = set(("electrical", "electricity", "power", "blackout", "wires", "phone", "pole", "poles", "outage", "outages", "wifi", "lose", "lost", "cuts", "cut"))
keywords_c = set(("trap", "stuck", "trapped", "underneath", "between"))
keywords_d = set(("blocked", "block", "road", "street", "avenue", "fallen", "tree", "pole"))
keywords_e = set(("fire", "flames", "smoke", "fires", "flame", "smoking", "ignited", "ignite"))

'''
a: flood damage
b: electrical issues 
c: people trapped
d: road blocked
e: fire
'''

def sanitize(text):
	words = text.split()
	final = []
	hashtags = []
	for word in words:
		if "http" not in word and "@" not in word:
			if "#" in word:
				clean = word.replace("#", "").lower()
				clean = "".join([x for x in clean if x.isalpha()])
				hashtags.append(clean)
				if clean != "":
					final.append(clean)
			else:
				clean = word.lower()
				clean = "".join([x for x in clean if x.isalpha()])
				if clean != "":
					final.append(clean)

	return final, hashtags

def categorize(word_list):
	categories = [0] * 6
	keys = 0
	for i in range(0, len(word_list)):
		if word_list[i] in keywords_a:
			categories[0] += 1
			keys += 1
		if word_list[i] in keywords_b:
			categories[1] += 1
			keys += 1
		if word_list[i] in keywords_c:
			categories[2] += 1
			keys += 1
		if word_list[i] in keywords_d:
			if "journal" not in word_list:
				categories[3] += 1
				keys += 1
		if word_list[i] in keywords_e:
			categories[4] += 1
			keys += 1
	c = 5
	val = 0
	for i in range(0, len(categories) - 1):
		if categories[i] > val:
			c = i
			val = categories[i]
	return c

if __name__ == '__main__':

	'''
	Categorizing the Relevant Tweets
	'''
	# Choose the relevant file based on which class is considered relevant according to the
	# initial_relevant_tweet we assigned above because we know it's relevant
	relevant_tweets = []
	line_counter = 0
	with open("relevant.txt") as relevant_file:
		tweet_author = ""
		tweet_text = "" 
		for line in relevant_file:
			if line_counter % 2 == 0:
				tweet = line.rstrip().replace("\n", "")
			elif line_counter % 2 != 0:
				words = line.rstrip().split(",")
				relevant_tweets.append([tweet, words])
			line_counter += 1
	print(relevant_tweets[0:100])
	count = 0
	categories = np.zeros((len(relevant_tweets), 7))
	clusters = np.zeros(len(relevant_tweets))
	for tweet in relevant_tweets:
		clusters[count] = categorize(tweet[1])
		count += 1

	with open("sorted_output.txt", "w+") as out:
		for i in range(0, 6):
			out.write("--------------CLUSTER " + str(i) + " ----------------" + "\n")
			for j in range(0, len(relevant_tweets)):
				if clusters[j] == i:
					out.write(relevant_tweets[j][0] + "\n")
			print(i)
	with open("output.txt", "w+") as out:
		count = 0
		for tweet in relevant_tweets:
			out.write(tweet[0] + "\n" + ",".join(tweet[1]) + "\n" + str(clusters[count]) + "\n")
			count += 1


		
		



				
