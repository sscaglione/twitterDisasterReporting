import json
import numpy as np
from sklearn import cluster
from sklearn.externals import joblib
#Read in tweets as json, create bag of words from sanitized text body
tweets = {}

keywords_primary = set(("hurricane", "sandy", "storm", "surge", "canceled"))
keywords_secondary = set(("surge", "canceled", "evac", "evacuate", "flood", "wind", "winds", "police", "authorities", "emerg", "emergency", "emergencies", "closing", "crisis"))
no_words = set(("glass", "hawker", "prayers", "campaign", "campaigns", "cheeks", "election", "nigga", "niggas", "ain't", "shit", "fuck", "gop", "u", "obama", "romney", "mittstormtips"))


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
	features = [0] * 5
	for i in range(0, len(word_list)):
		if word_list[i] in keywords_primary:
			features[0] += 1
		if word_list[i] in keywords_secondary:
			features[1] += 1
			features[0] += 1
		if word_list[i] in no_words:
			features[2] += 1
	if "hurricane" in word_list and "sandy" not in word_list:
		features[0] -= 1
	if "sandy" in word_list and "hurricane" not in word_list:
		features[0] -= 1
	chars = sum([len(x) for x in word_list])
	features[3] = len(word_list)
	features[4] = float(chars) / len(word_list)
	return features

if __name__ == '__main__':	
	clusts = None
	row_to_id = {}
	with open("29Oct2012-31Oct2012.json") as f:
		for line in f:
			try:
				t = json.loads(line)
				if t['text']:
					text = t['text'].replace("\n", " ")
					words, tags = sanitize(text)
					if t['from_user_name'] != 0:
						tweets[t["id"]] = (words, tags, text, t['from_user_name'])
					else:
						tweets[t["id"]] = (words, tags, text, "json issues")
			except ValueError as e:
				pass
		
	features = np.zeros((len(tweets), 5))
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
	test = np.array(gen_features(sanitize(initial_relevant_tweet)[0]))
	test = test.reshape(1, -1)
	print(test)
	print("TEST Y")
	test_y = mbk.predict(test)
	print(test_y)
	pos_class = 0
	with open("relevant.txt", "w+") as out:
			for i in range(len(clusts)):
				t = row_to_id[i]				
				if clusts[i] == test_y:
					pos_class += 1
					out.write(tweets[t][2] + "\n" + ",".join(tweets[t][0]) + "\n")
	neg_class = len(clusts) - pos_class
	percent_removed = 10 * float(neg_class) / len(clusts)
	#print(str(percent_removed) + "% of tweets removed as noise")
	#print(mbk.cluster_centers_)
	x = np.array([5, 5, 0, 15, 6]).reshape(1, -1)
	print("TRIAL Y")
	print(mbk.predict(x)[0])
	joblib.dump(mbk, "cluster_model.pkl")

