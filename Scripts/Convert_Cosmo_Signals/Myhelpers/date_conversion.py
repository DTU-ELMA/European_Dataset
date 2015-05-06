import datetime

def parse_datetime_string(s):
	y,m,d,h = int(s[3:7]),int(s[7:9]),int(s[9:11]),int(s[11:13])
	return datetime.datetime(y,m,d,h)

def write_datetime_string(d):
	return '{0:04d}{1:02d}{2:02d}{3:02d}'.format(d.year,d.month,d.day,d.hour)
