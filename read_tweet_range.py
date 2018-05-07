#Create file with subset of tweets from specific range of dates

from datetime import datetime
start_date = "29 Oct 2012"
end_date =  "31 Oct 2012"

with open("/home/mara/Downloads/sandy_hurricane.txt") as tweets_file:
	with open(start_date.replace(" ", "")+"-"+end_date.replace(" ", "")+".txt", "w+") as out:
		for line in tweets_file:
			s = line.split("created_at")[1][9:20]
			d = datetime.strptime(s, '%d %b %Y')
			if ((d >=  (datetime.strptime(start_date, '%d %b %Y'))) and (d <=(datetime.strptime(end_date, '%d %b %Y')))):
				out.write(line)
			if (d > (datetime.strptime(end_date, '%d %b %Y'))):
				break