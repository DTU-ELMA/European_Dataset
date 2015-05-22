import numpy as np
import pygrib as pg
from scipy.spatial import cKDTree

# Load grid from data
fH = pg.open('metadata/HHL.grb')
dlat, dlon = fH[1].latlons()

# Load high-resolution countries grid
fc = np.load('countries-interpolator.npz')
c_lats = fc['lats']
c_lons = fc['lons']
countries = fc['countries']

# Load high-resolution onshore grid
f2 = np.load('onshore-interpolator.npz')
o_lats = f2['lats']
o_lons = f2['lons']
onshore = np.invert(f2['onshore'])

# Construct K-dimensional tree for fast lookup
c_points = np.array((c_lons.flatten(), c_lats.flatten())).T
flatcountries = countries.flatten()
c_tree = cKDTree(c_points)

o_points = np.array((o_lons.flatten(), o_lats.flatten())).T
flatonshore = onshore.flatten()
o_tree = cKDTree(o_points)

# Construct points for lookup from data grid
outpoints = np.array((dlon.flatten(), dlat.flatten())).T

# ...and go!
# Finding nearest neighbours for 700k points among 57M candidates
# in < 2sec. Science!
c_dis, c_idx = c_tree.query(outpoints, eps=10**-4, distance_upper_bound=1)
o_dis, o_idx = o_tree.query(outpoints, eps=10**-4, distance_upper_bound=1)


# Reconstruct onshore grid and save
f = np.reshape(flatcountries[c_idx-1], dlat.shape)

code = {'ALB': 240,
		'AND': 239, 
		'AUT': 229,
		'BEL': 226,
		'BGR': 221,
		'BIH': 219,
		'BLR': 33,
		'CHE': 205,
		'CZE': 187,
		'DEU': 186,
		'DNK': 183,
		'ESP': 177,
		'EST': 122,
		'FIN': 174,
		'FRA': 171,
		'FRO': 170,
		'GBR': 167,
		'GRC': 157,
		'GRL': 155,
		'HRV': 149,
		'HUN': 246,
		'IRL': 146,
		'ITA': 1,
		'ISL': 143,
		'JEY': 140,
		'LAT': 218,
		'LUX': 121,
		'MCO': 171,
		'MKD': 111,
		'MNE': 108,
		'MOL': 116,
		'NOR': 4,
		'NLD': 91,
		'POL': 79,
		'POR': 76,
		'ROU': 71,
		'RUS': 6,
		'SJM': 63,
		'SRB': 56,
		'SVK': 53,
		'SVN': 52,
		'SWE': 51,
		'TUR': 37,
		'UKR': 33,
		}

dcountries = np.empty([f.shape[0], f.shape[1]], dtype="S3")

for i in range(f.shape[0]):
	print i
	for j in range(f.shape[1]):
		for key in code:
			if int(f[i][j]) == code[key]:
				dcountries[i][j] = key
				break
			dcountries[i][j] = 'WAT'

donshore = np.reshape(flatonshore[o_idx], dlat.shape)

#donshore = np.load('onshore_COSMO.npz')['onshore']
dheights = np.load('heights.npy')

# countries_final = np.reshape(fcountries, (f.shape[0], f.shape[1]))

np.savez_compressed('geography_COSMO.npz', lats=dlat, lons=dlon, countries=dcountries, num_countries = f, onshore = donshore, heights=dheights )
