import numpy as np

def latlonstospace(lats,lons):
	lats = np.deg2rad(90 - lats)
	lons = np.deg2rad(lons)
	return np.array([np.sin(lats)*np.cos(lons), np.sin(lats)*np.sin(lons), np.cos(lats)]).T
