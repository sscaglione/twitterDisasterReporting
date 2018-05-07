from datetime import datetime, date, time, timedelta

import string
import time
import os

dialation = 1
start_time_s = "27 Oct 2012 18:45:54"
start_time = datetime.strptime(start_time_s, '%d %b %Y %H:%M:%S')

output_file = open("new.txt", "w+", os.O_NONBLOCK)

with open("3hour.txt") as tweets_file:
	for line in tweets_file:
		print(line)
		tweet_time_s = line.split("created_at")[1][9:29]
		tweet_time = datetime.strptime(tweet_time_s, '%d %b %Y %H:%M:%S')
		print(str(tweet_time), str(start_time))
		if (tweet_time <= start_time):
			print("in")
			output_file.write(line)
		else:
			time.sleep(dialation)
			start_time += timedelta(seconds=1)

