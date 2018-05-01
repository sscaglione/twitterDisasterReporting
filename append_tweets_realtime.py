from datetime import datetime

import string
import time

start_time_s = "27 Oct 2012 13:36:08"
start_time = datetime.strptime(start_time_s, '%d %b %Y %H:%M:%S')
end_time_s = "27 Oct 2012 13:37:08"
end_time = datetime.strptime(end_time_s, '%d %b %Y %H:%M:%S')

with open("sandy_sample.txt") as tweets_file:
	while (end_time > start_time):
		for line in tweets_file:
			s = line.split("created_at")[1][9:29]
			d = datetime.strptime(s, '%d %b %Y %H:%M:%S')
			if (d <= start_time):
				print(line)
		time.sleep(1)
		start_time += datetime.timedelta(0,1)
