import json
import numpy as np
from sklearn import cluster
#Read in tweets as json, create bag of words from sanitized text body
tweets = {}

keywords_primary = set(("hurricane", "sandy", "storm", "surge", "canceled"))
keywords_secondary = set(("surge", "canceled", "evac", "evacuate", "flood", "wind", "winds", "police", "authorities", "emerg", "emergency", "emergencies", "closing", "crisis"))
no_words = set(("glass", "hawker", "prayers", "campaign", "campaigns", "cheeks", "election", "nigga", "niggas", "ain't", "shit", "fuck", "gop", "u", "obama", "romney"))

keywords_a = set(("flood", "flooding", "flooded", "water", "overflow", "flow", "stream", "river", "overflowed", "soaked"))
keywords_b = set(("electrical", "electricity", "power", "blackout", "wires", "phone", "pole", "poles"))
keywords_c = set(("trap", "stuck", "trapped", "underneath", "between"))
keywords_d = set(("blocked", "block", "road", "street", "avenue", "fallen", "tree", "pole"))
keywords_e = set(("fire", "flames", "smoke", "fires", "flame", "smoking", "ignited", "ignite"))

# Relevant tweet
initial_relevant_tweet = "RT @newsday: Evacuation ordered for Fire Island as Hurricane #Sandy approaches http://t.co/0pTTrYoF"


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

	#print(words, final, hashtags)
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

def gen_categories(word_list):
	categories = [0] * 2
	for i in range(0, len(word_list)):
		if word_list[i] in keywords_a:
			categories[0] += 1

	categories[1] = len(word_list)
	return categories

clusts = None
row_to_id = {}
with open("sandy_2.json") as f:
	for line in f:
		try:
			t = json.loads(line)
			#print(t['text'])
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
	#print(len(row_to_id))
	mbk = cluster.MiniBatchKMeans(n_clusters=2)
	clusts = mbk.fit_predict(features)


relevant_class = 0
with open("class_0.txt", "w+") as out0:
	with open("class_1.txt", "w+") as out1:
		count = 0
		for i in range(len(clusts)):
			t = row_to_id[i]
			
			if clusts[i] == 0:
				out0.write(tweets[t][3] + "\n" + tweets[t][2] + "\n")
			else:
				if tweets[t][2] == initial_relevant_tweet:
					relevant_class = 1
				out1.write(tweets[t][3] + "\n" + tweets[t][2] + "\n")
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
			tweet_text = line
			relevant_tweets.append({	"tweet_author": 	tweet_author, 
							"tweet_text": 		tweet_text})
		line_counter += 1

count = 0
categories = np.zeros((len(tweets), 6))
for tweet_dict in relevant_tweets:
	x = gen_categories(tweet_dict["tweet_text"])
	for i in range(0, len(x)):
		categories[count, i] = x[i]
	count += 1
mbk = cluster.MiniBatchKMeans(n_clusters = 5)
clusts = mbk.fit_predict(categories)
'''
for i in range(len(clusts)):
	if clusts[i] == 1:
		print(relevant_tweets[i]["tweet_text"])
		'''
		



				
