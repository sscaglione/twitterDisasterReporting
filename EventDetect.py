import datetime as dt
import sys

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

	def insert(self, t):
		words = frozenset(t[0])
		tweet = t[1]
		cat = t[2]
		if cat == 5:
			return
		c = self.closest_match(words, cat)
		if c[1] > 0.8:
			key = words.union(c[0])
			if key == c[0]:
				self.tweets[cat][c[0]][0].append(tweet)
				if len(self.tweets[cat][c[0]][0]) >= self.threshold:
					self.new_event(c[0], self.tweets[cat][c[0]])
					self.tweets[cat][c[0]][2] = 1
			else:
				t_list = self.tweets[cat][c[0]][0]
				t_list.append(tweet)
				if len(t_list) >= self.threshold:
					self.new_event(c[0], self.tweets[cat][c[0]])
					self.tweets[cat][c[0]][2] = 1
				self.tweets[cat][key] = [t_list, self.tweets[cat][c[0]][1], self.tweets[cat][c[0]][2]]
				del self.tweets[cat][c[0]]
		else:
			self.tweets[cat][words] = [[tweet], dt.datetime.now(), 0]

	def prune(self, time):
		new_tweets = {}
		for c in tweets:
			for t in c:
				if tweets[c][t][1] >= time:
					new_tweets[c][t] = tweets[c][t]
		self.tweets = new_tweets
	def new_event(self, k, t):
		if not t[2]:
			print(k)
			print(t)
			line = t[0][0] + "\t" + str(t[1]) + "\n"
			with open("events.txt", "a+") as out:
				out.write(line)
			#print(self.tweets[k])

if __name__ == '__main__':
	ed = EventDetect(5)
	#insert()
	count = 1
	with open("sample.txt") as f:
		line = 1
		line = f.readline().rstrip()
		while(line):
			tweet = line
			line = f.readline()
			words = frozenset(line.rstrip().split(","))
			line = f.readline()
			cat = int(float(line.rstrip()))
			t = [words, tweet, cat]
			ed.insert(t)
			count += 1
			line = f.readline().rstrip()

	"""print(len(ed.tweets))
	for i in ed.tweets:
		print(len(i))
		for e in i:
			print(e)"""
