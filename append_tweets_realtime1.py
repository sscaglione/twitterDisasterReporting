from datetime import datetime, date, time, timedelta

import string
import time

start_time_s = "27 Oct 2012 13:36:08"
start_time = datetime.strptime(start_time_s, '%d %b %Y %H:%M:%S')

with open("sandy_sample.txt") as tweets_file:
	for line in tweets_file:
		tweet_time_s = line.split("created_at")[1][9:29]
		tweet_time = datetime.strptime(tweet_time_s, '%d %b %Y %H:%M:%S')
		if (tweet_time <= start_time):
			print(line)
		elif (d > start_time):
			td = d - start_time #td = timedelta
			time.sleep(td.total_seconds())
			start_time += td
			print(line)
