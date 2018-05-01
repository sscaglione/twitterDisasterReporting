from datetime import datetime

import string
import time

start_time = "27 Oct 2012 13:36:22"

with open("sandy_sample.txt") as tweets_file:
	for line in tweets_file:
		s = line.split("created_at")[1][9:29]
		d = datetime.strptime(s, '%d %b %Y %H:%M:%S')
		if (d <= (datetime.strptime(start_time, '%d %b %Y %H:%M:%S'))):
			print(line)
		elif (d > (datetime.strptime(start_time, '%d %b %Y %H:%M:%S'))):
			td = d - (datetime.strptime(start_time, '%d %b %Y %H:%M:%S')) #td = timedelta
			time.sleep(td.total_seconds())
			start_time += td
			print(line)
