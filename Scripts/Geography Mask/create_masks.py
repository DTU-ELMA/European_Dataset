import numpy as np
import matplotlib.pyplot as plt

geography = np.load('geography_COSMO.npz')
lats = geography['lats']
lons = geography['lons']
countries = geography['countries']
onshore = geography['onshore']
heights = geography['heights']

windmask = np.empty([lats.shape[0], lons.shape[1]], dtype=bool)
solarmask = np.empty([lats.shape[0], lons.shape[1]], dtype=bool)

for i in range(lats.shape[0]):
	for j in range(lats.shape[1]):
		c = countries[i][j]
		if (c == 'ALB' or c == 'AUT' or c == 'BEL' or c == 'BGR' or c == 'BIH' or c == 'CHE' or c == 'CZE' or c == 'DEU' or c == 'DNK' or c == 'ESP' or \
			c == 'FRA' or c == 'GRC' or c == 'HRV' or c == 'HUN' or c == 'ITA' or c == 'LUX' or c == 'MKD' or c == 'MNE' or c == 'NLD' or c == 'POL' or \
			c == 'POR' or c == 'ROU' or c == 'SRB' or c == 'SVK' or c == 'SVN'):
			if onshore[i][j] == True:
				windmask[i][j] = True
				solarmask[i][j] = True
			elif  heights[i][j] >= -70:
				windmask[i][j] = True
				solarmask[i][j] = False
			else:
				solarmask[i][j] = False
				windmask[i][j] = False
		else:
			solarmask[i][j] = False
			windmask[i][j] = False

np.save('../../Data/Metadata/lats_COSMO.npy', lats)
np.save('../../Data/Metadata/lons_COSMO.npy', lons)
np.save('../../Data/Metadata/onshore_COSMO.npy', onshore)
np.save('../../Data/Metadata/windmask_COSMO.npy', windmask)
np.save('../../Data/Metadata/solarmask_COSMO.npy', solarmask)
