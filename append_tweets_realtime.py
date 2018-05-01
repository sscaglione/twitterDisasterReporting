from datetime import datetime

import string

start_time = ###

with open("sandy_hurricane.txt") as tweets_file:
	for line in tweets_file:
		s = line.split("created_at")[1][9:28]
		d = datetime.strptime(s, '%d %b %Y %H %M %S')))
		if (d <= (datetime.strptime(start_time, '%d %b %Y %H %S')):
			sys.stdout.write(line)
		elif (d > (datetime.strptime(start_time, '%d %b %Y %H %S')):
			td = d - start_time #td = timedelta
			time.sleep(td.total_seconds())
			start_time += td
			sys.stdout.write(line)
