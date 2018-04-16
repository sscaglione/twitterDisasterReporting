import json
import numpy as np
from sklearn import cluster
#Read in tweets as json, create bag of words from sanitized text body
tweets = {}

keywords_primary = set(("hurricane", "sandy", "storm", "surge", "canceled"))
keywords_secondary = set(("surge", "canceled", "evac", "evacuate", "flood", "wind", "winds", "police", "authorities", "emerg", "emergency", "emergencies", "closing", "crisis"))
no_words = set(("glass", "hawker", "prayers", "campaign", "campaigns", "cheeks", "election", "nigga", "niggas", "ain't", "shit", "fuck", "gop", "u", "obama", "romney"))

keywords_a = set(("flood", "flooding", "flooded"))
keywords_a_secondary = set(("overflow", "flow", "stream", "river", "overflowed", "soaked", "level"))
keywords_b = set(("electrical", "electricity", "power", "blackout", "wires", "phone", "pole", "poles", "outage", "outages", "wifi"))
keywords_c = set(("trap", "stuck", "trapped", "underneath", "between"))
keywords_d = set(("blocked", "block", "road", "street", "avenue", "fallen", "tree", "pole"))
keywords_e = set(("fire", "flames", "smoke", "fires", "flame", "smoking", "ignited", "ignite"))

# Relevant tweet
initial_relevant_tweet = "IF I LOSE POWER FOR A WEEK FROM THIS HURRICANE LIKE I DID LAST YEAR I'LL BE PISSED"


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
def gen_features(word_list):
	features = [0] * 4
	for i in range(0, len(word_list)):
		if word_list[i] in keywords_primary:
			features[0] += 1
		if word_list[i] in keywords_secondary:
			features[1] += 1
		if word_list[i] in no_words:
			features[2] += 1
		if "hurricane" in word_list[i] and "sandy" not in word_list[i]:
			features[0] -= 1
	features[3] = len(word_list)
	return features

def categorize(word_list):
	categories = [0] * 6
	keys = 0
	for i in range(0, len(word_list)):
		if word_list[i] in keywords_a:
			categories[0] += 1
			keys += 1
		if word_list[i] in keywords_a_secondary:
			categories[0] += 1
			keys += 0.5
		if word_list[i] in keywords_b:
			categories[1] += 1
			keys += 1
		if word_list[i] in keywords_c:
			categories[2] += 1
			keys += 1
		if word_list[i] in keywords_d:
			categories[3] += 1
			keys += 1
		if word_list[i] in keywords_e:
			categories[4] += 1
			keys += 1
	c = 6
	val = 0
	for i in range(0, len(categories) - 1):
		if categories[i] > val:
			c = i
			val = categories[i]
	"""if c == 0:
		print(word_list)
		print(categories)
		print(c)"""
	return c

clusts = None
row_to_id = {}
with open("sandy_2.json") as f:
	for line in f:
		try:
			t = json.loads(line)
			if t['text']:
				words, tags = sanitize(t['text'])
				if t['from_user_name'] != 0:
					tweets[t["id"]] = (words, tags, t['text'], t['from_user_name'])
				else:
					tweets[t["id"]] = (words, tags, t['text'], "json issues")
		except ValueError as e:
			pass
	features = np.zeros((len(tweets), 4))
	count = 0
	for t in tweets:
		row_to_id[count] = t
		features[count, 0] = t
		x = gen_features(tweets[t][0])
		for i in range(0, len(x)):
			features[count, i] = x[i]
		count += 1
	mbk = cluster.MiniBatchKMeans(n_clusters=2)
	clusts = mbk.fit_predict(features)


relevant_class = 0
with open("class_0.txt", "w+") as out0:
	with open("class_1.txt", "w+") as out1:
		count = 0
		for i in range(len(clusts)):
			t = row_to_id[i]
			
			if clusts[i] == 0:
				if tweets[t][2] == initial_relevant_tweet:
					print("Relevant class is class 0")
					relevant_class = 0
				out0.write(tweets[t][2] + "\n")
			else:
				if tweets[t][2] == initial_relevant_tweet:
					print("Relevant class is class 1")
					relevant_class = 1
				out1.write(tweets[t][2] + "\n")
				count += 1

'''
Categorizing the Relevant Tweets
'''
# Choose the relevant file based on which class is considered relevant according to the
# initial_relevant_tweet we assigned above because we know it's relevant
relevant_file_name = "class_0.txt"
if relevant_class == 1:
	relevant_file_name = "class_1.txt"

# Read the relevant tweets into a list of dictionaries
relevant_tweets = []
line_counter = 0
with open(relevant_file_name) as relevant_file:
	tweet_author = ""
	tweet_text = ""
	for line in relevant_file:
		if line_counter % 2 == 0:
			tweet_author = line
		elif line_counter % 2 != 0:
			tweet_text = sanitize(line.rstrip())[0]
			if len(tweet_text):
				relevant_tweets.append((tweet_text, line.rstrip()))
		line_counter += 1

count = 0
categories = np.zeros((len(tweets), 7))
clusters = np.zeros(len(tweets))
for tweet in relevant_tweets:
	clusters[count] = categorize(tweet[0])
	count += 1


"""relevant_a = []
irrelevant_a = []
print("Length of relevant tweets: ", len(relevant_tweets))
print("Length of clusts: ", len(clusters))
for i in range(len(clusters)):
	if clusters[i] == 0:
		relevant_a.append(relevant_tweets[i]["tweet_text"])
	else:
		irrelevant_a.append(relevant_tweets[i]["tweet_text"])

print(irrelevant_a[0:3])
print(relevant_a[0:3])"""
with open("output.txt", "w+") as out:
	for i in range(0, 7):
		out.write("--------------CLUSTER " + str(i) + " ----------------" + "\n")
		for j in range(0, len(relevant_tweets)):
			if clusters[j] == i:
				out.write(relevant_tweets[j][1] + "\n")
		print(i)


		
		



				
