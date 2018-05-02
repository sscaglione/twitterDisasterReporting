import datetime as dt
import sys
from time import sleep
from sklearn.externals import joblib
from tweet_to_json import tweet_to_json
from build_cluster import sanitize, gen_features
import numpy as np
import json
from tweet_cluster_naive import categorize
from datetime import datetime, date, timedelta
import os


class EventDetect:
	def __init__(self, threshold):
		self.threshold = threshold
		self.common_ignore = set(["the", "to", "of", "and", "a", "is", "in", "that", "I"])
		self.categories = 6
		self.tweets = [{}]
		for i in range(0, self.categories - 1):
			self.tweets += [{}]
		print(self.tweets)
		#tweets[s] = [[tweet1, tweet2, ...], category, earliest_time]
	def jaccard(self, bag1, bag2):
		same = bag1.intersection(bag2)
		total = bag1.union(bag2)
		same = [x for x in same if x not in self.common_ignore]
		total = [x for x in total if x not in self.common_ignore]
		return float(len(same)) / len(total)

	def closest_match(self, words, category):
		max_sim = 0
		key = -1
		for c in self.tweets[category]:
			score = self.jaccard(words, c)
			if score > max_sim:
				max_sim = score
				key = c
		return((key, max_sim))
		#key_match, score

	def insert(self, t, timestamp, user):
		words = frozenset(t[0])
		tweet = t[1]
		cat = t[2]
		if cat == 5:
			return
		c = self.closest_match(words, cat)
		if c[1] > 0.7:
			key = words.union(c[0])
			if key == c[0]:
				self.tweets[cat][c[0]][0].append(tweet)
				if len(self.tweets[cat][c[0]][0]) >= self.threshold:
					self.new_event(c[0], self.tweets[cat][c[0]], cat, user)
					self.tweets[cat][c[0]][2] = 1
			else:
				t_list = self.tweets[cat][c[0]][0]
				t_list.append(tweet)
				if len(t_list) >= self.threshold:
					self.new_event(c[0], self.tweets[cat][c[0]], cat, user)
					self.tweets[cat][c[0]][2] = 1
				self.tweets[cat][key] = [t_list, self.tweets[cat][c[0]][1], self.tweets[cat][c[0]][2]]
				del self.tweets[cat][c[0]]
		else:
			self.tweets[cat][words] = [[tweet], timestamp, 0]

	def prune(self, time):
		new_tweets = {}
		for c in tweets:
			for t in c:
				if tweets[c][t][1] >= time:
					new_tweets[c][t] = tweets[c][t]
		self.tweets = new_tweets
	def new_event(self, k, t, c, u):
		print("Is it new?")
		print(t[2])
		if not t[2]:
			line = t[0][0] + "\t" + u + "\t" + str(t[1]) + "\t" + str(c) + "\t0.75\n"
			with open("events.txt", "a+", os.O_NONBLOCK) as out:
				out.write(line)
			print(line)

if __name__ == '__main__':
	ed = EventDetect(3)
	dialation = 0.01
	#insert()
	count = 1
	km = joblib.load("cluster_model.pkl")
	x = np.array([5, 5, 0, 15, 6]).reshape(1, -1)
	relevant = km.predict(x)[0]
	with open("3hour.txt") as f:
		line = 1
		line = f.readline().rstrip()
		tweet_time_s = line.split("created_at")[1][9:29]
		current_time = datetime.strptime(tweet_time_s, '%d %b %Y %H:%M:%S')
		while(line):
			tweet_time_s = line.split("created_at")[1][9:29]
			tweet_time = datetime.strptime(tweet_time_s, '%d %b %Y %H:%M:%S')
			print(tweet_time, current_time)
			if tweet_time > current_time:
				sleep(dialation)
				current_time += timedelta(seconds=1)
			line = tweet_to_json(line)
			user = "Unknown"
			try:
				t = json.loads(line)
				if t['text']:
					text = t['text'].replace("\n", " ")
					words, tags = sanitize(text)
					if t['from_user_name'] != 0:
						line = (words, tags, text, t['from_user_name'])
						user = t['from_user_name']
					else:
						line = (words, tags, text, "json issues")
			except ValueError as e:
				line = f.readline().rstrip()
				continue
			x = np.array(gen_features(line[0])).reshape(1, -1)
			r = km.predict(x)[0]
			if r != relevant:
				line = f.readline().rstrip()
				continue
			c = categorize(line[0])
			if c == 5:
				line = f.readline().rstrip()
				continue
			words = frozenset(line[0])
			t = [words, line[2], c]
			ed.insert(t, tweet_time, user)
			count += 1
			line = f.readline().rstrip()
			print(count)

	"""print(len(ed.tweets))
	for i in ed.tweets:
		print(len(i))
		for e in i:
			print(e)"""
