"""Event detect streams in tweets in realtime
i.e. The first tweet will be read immediately. If the second tweet's timestamp is 3 seconds after the first, it will be processed 3 seconds after the first was processed.
This allows simulation of realtime data.
Inserting a tweet into the Event Detect class puts it in a bin with similar tweets or starts a new bin.
When a bin meets certain criteria, it is classified as an event, and output to a file.

Note: Currently EventDetect and the server are interfacing by file I/O. It is a goal to rewrite this code to use sockets.
Due to having 2 scripts using the same file, files are opened with os.O_NONBLOCK. This may not work on non-Linux systems.
"""


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
		self.common_ignore = set(["the", "to", "of", "and", "a", "is", "in", "that", "I"])		#Similarity between tweets is Jaccard distance but will not include the most common words to lessen superficial similarity
		self.categories = 6
		self.tweets = [{}]
		#tweets[c][b] = [[tweet1, tweet2, ...], category, earliest_time, detected]
		#"tweets of category c in bucket b" = "all tweets in bucket, category c, time of first tweet, has this bucket already been detected as an event"
		for i in range(0, self.categories - 1):
			self.tweets += [{}]
		print(self.tweets)

	def jaccard(self, bag1, bag2):
		same = bag1.intersection(bag2)
		total = bag1.union(bag2)
		same = [x for x in same if x not in self.common_ignore]
		total = [x for x in total if x not in self.common_ignore]
		return float(len(same)) / len(total)

	def closest_match(self, words, category):
		#Return key of most similar bucket
		max_sim = 0
		key = -1
		for c in self.tweets[category]:
			score = self.jaccard(words, c)
			if score > max_sim:
				max_sim = score
				key = c
		return((key, max_sim))

	def insert(self, t, timestamp, user):
		words = frozenset(t[0])
		tweet = t[1]
		cat = t[2]
		#Category 5 == "No category" so don't insert
		if cat == 5:
			return
		#Find closest match, put new tweet into bucket, test for event conditions
		c = self.closest_match(words, cat)
		if c[1] > 0.7:
			#Generate new key based on words in bucket and words in new tweet
			key = words.union(c[0])
			#If new key is the same as the old key, just append new tweet in existing bucket
			if key == c[0]:
				self.tweets[cat][c[0]][0].append(tweet)
				if len(self.tweets[cat][c[0]][0]) >= self.threshold:
					self.new_event(c[0], self.tweets[cat][c[0]], cat, user)
					self.tweets[cat][c[0]][2] = 1		#Flip value to show event has been detected
			#Else create new bucket that is combo of bucket + new tweet, delete old bucket
			else:
				t_list = self.tweets[cat][c[0]][0]
				t_list.append(tweet)
				if len(t_list) >= self.threshold:
					self.new_event(c[0], self.tweets[cat][c[0]], cat, user)
					self.tweets[cat][c[0]][2] = 1		#Flip value to show event has been detected
				self.tweets[cat][key] = [t_list, self.tweets[cat][c[0]][1], self.tweets[cat][c[0]][2]]
				del self.tweets[cat][c[0]]
		#If no closest match, create new bucket
		else:
			self.tweets[cat][words] = [[tweet], timestamp, 0]

	def prune(self, time):
		#Currently unused
		#Remove buckets with initial timestamp before time
		new_tweets = {}
		for c in tweets:
			for t in c:
				if tweets[c][t][1] >= time:
					new_tweets[c][t] = tweets[c][t]
		self.tweets = new_tweets

	def new_event(self, k, t, c, u):
		#Input: key, time, category, user
		print("Is it new?")
		print(t[2])			#Test if bucket has been written before
		#Write bucket info to file for access by server
		if not t[2]:
			line = t[0][0] + "\t" + u + "\t" + str(t[1]) + "\t" + str(c) + "\t0.75\n"
			with open("events.txt", "a+", os.O_NONBLOCK) as out:
				out.write(line)
			print(line)

if __name__ == '__main__':
	ed = EventDetect(3)		#Param is # of tweets to trigger an event
	dialation = 0.01		#Allow accelerated throughput of tweet playback (eg 0.01 means 1 second between timestamps is 1/100 second of real time)
	count = 1
	km = joblib.load("cluster_model.pkl")			#Load noise removal model
	x = np.array([5, 5, 0, 15, 6]).reshape(1, -1)	#Generate test instance (test instance is known relevant class. Only process tweets with same class value)
	relevant = km.predict(x)[0]
	with open("10hour.txt") as f:
		line = 1
		line = f.readline().rstrip()
		tweet_time_s = line.split("created_at")[1][9:29]
		current_time = datetime.strptime(tweet_time_s, '%d %b %Y %H:%M:%S')
		while(line):
			#generate datetime object, perform "realtime" playback using sleep
			tweet_time_s = line.split("created_at")[1][9:29]
			tweet_time = datetime.strptime(tweet_time_s, '%d %b %Y %H:%M:%S')
			if tweet_time > current_time:
				sleep(dialation)
				current_time += timedelta(seconds=1)
			line = tweet_to_json(line)
			user = "Unknown"
			#Import and fix json objects
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
			#Handle json objects that could not be fixed
			except ValueError as e:
				line = f.readline().rstrip()
				continue
			#Generate features for tweet, classify as relevant/noise
			x = np.array(gen_features(line[0])).reshape(1, -1)
			r = km.predict(x)[0]
			if r != relevant:					#If not relevant, don't insert
				line = f.readline().rstrip()
				continue
			c = categorize(line[0])				#If category 5, "no category," don't insert
			if c == 5:
				line = f.readline().rstrip()
				continue
			#Generate object for insertion and insert into EventDetect class
			words = frozenset(line[0])
			t = [words, line[2], c]
			ed.insert(t, tweet_time, user)
			count += 1
			line = f.readline().rstrip()
			print(count)
