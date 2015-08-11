import datetime

def parse_datetime_string(s):
	y,m,d,h = int(s[:4]),int(s[4:6]),int(s[6:8]),int(s[8:10])
	return datetime.datetime(y,m,d,h)

def write_datetime_string(d):
	return '{0:04d}{1:02d}{2:02d}{3:02d}'.format(d.year,d.month,d.day,d.hour)