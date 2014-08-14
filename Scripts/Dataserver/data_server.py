import datetime
import numpy as np

# Class which can have attributes set.
class expando(object): pass

class Dataserver:
	'''
		Loads in and serves data between the dates indicated.
		Forecast is returned for firstday for the period from
		firstday + day_ahead_delta until day_ahead_period later.
	'''
	
	def __init__(self,firstday=datetime.datetime(2012,01,01,00),lastday=datetime.datetime(2012,01,03,00),day_ahead_delta=24,day_ahead_period=24, forecastdir='../../Data/nodal_fc', signaldir='../../Data/nodal_ts', \
windforecastfilename='WNDpower_onshore-V90_3MW_offshore-V164_7MW_offshore.npz', \
solarforecastfilename='PVpower_Scheuten215IG.npz', \
windsignalfilename='WNDpower_onshore-V90_3MW_offshore-V164_7MW_offshore-{0:04d}{1:02d}.npz', \
solarsignalfilename='PVpower_Scheuten215IG-{0:04d}{1:02d}.npz', \
loadsignalfilename='load-{0:04d}{1:02d}.npz'):
		self.firstdate = firstday
		self.curdate = firstday
		self.lastdate = lastday
		self.dadelta = day_ahead_delta
		self.datimedelta = datetime.timedelta(hours=day_ahead_delta)
		self.period = day_ahead_period
		self.timeperiod = datetime.timedelta(hours=day_ahead_period)
		
		self.files = expando()
		self.files.fcdir = forecastdir
		self.files.tsdir = signaldir
		self.files.windfc = windforecastfilename
		self.files.solarfc = solarforecastfilename
		self.files.windts = windsignalfilename
		self.files.solarts = solarsignalfilename
		self.files.loadts = loadsignalfilename
		self.files.fcdirformat = '{0:04d}{1:02d}{2:02d}{3:02d}'
		
		self.cache = expando()
		
	def next(self):
		if self.curdate > self.lastdate:
			raise StopIteration
		self.curdate += self.timeperiod
		return self.load_current_data()
	
	def __reset__(self):
		self.curdate = self.firstdate
	
	def load_current_data(self):
		'''
			Returns data for the current date/time.
			Out: ((times_fc,wind_fc, solar_fc),(times_ts,wind_ts, solar_ts, load_ts))
		'''
		return (self.load_current_forecasts(),self.load_current_signals())
	
	def load_current_forecasts(self):
		curfcdir = self.files.fcdirformat.format(self.curdate.year, self.curdate.month, self.curdate.day, self.curdate.hour)
		wind_fc = np.load(self.files.fcdir + '/' + curfcdir +'/' + self.files.windfc)
		times_fc, wind_fc = wind_fc['dates'],wind_fc['data']
		solar_fc = np.load(self.files.fcdir + '/' + curfcdir + '/' + self.files.windfc)
		solar_fc = solar_fc['data']
		return (times_fc[self.dadelta:self.dadelta + self.period],wind_fc[self.dadelta:self.dadelta + self.period], solar_fc[self.dadelta:self.dadelta + self.period])
	
	def load_current_signals(self):
		tsdate = self.curdate + self.datimedelta
		wind_ts = np.load(self.files.tsdir + '/' + self.files.windts.format(tsdate.year,tsdate.month))
		times_ts, wind_ts = wind_ts['dates'],wind_ts['data']
		indx = times_ts.tolist().index(tsdate)
		solar_ts = np.load(self.files.tsdir + '/' + self.files.solarts.format(tsdate.year,tsdate.month))
		solar_ts = solar_ts['data']
		load_ts = np.load(self.files.tsdir + '/' + self.files.loadts.format(tsdate.year,tsdate.month))
		load_ts = load_ts['data']
		return (times_ts[indx:indx+ self.period],wind_ts[indx:indx+ self.period],solar_ts[indx:indx+ self.period],load_ts[indx:indx+ self.period])

