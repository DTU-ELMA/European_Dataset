import numpy as np

geography = np.load('geography_COSMO.npz')
lats = geography['lats']
lons = geography['lons']
countries = geography['countries']
onshore = geography['onshore']
heights = geography['heights']

# Country codes that will be included in the mask.
includedcountries = {
    'ALB', 'AUT', 'BEL', 'BGR', 'BIH',
    'CHE', 'CZE', 'DEU', 'DNK', 'ESP', 'FRA',
    'GRC', 'HRV', 'HUN', 'ITA', 'LUX', 'MKD',
    'MNE', 'NLD', 'POL', 'POR', 'ROU', 'SRB',
    'SVK', 'SVN'}

# Initialize arrays of False
windmask = np.zeros(lats.shape, dtype=bool)
solarmask = np.zeros(lats.shape, dtype=bool)

for ix, c in np.ndenumerate(countries):
    if (c in includedcountries):
        if onshore[ix]:
            # If onshore, we can use the area for wind and solar.
            windmask[ix] = True
            solarmask[ix] = True
        elif heights[ix] >= -70:
            # If offshore and sea depth is less than 70m, we can use the area for wind.
            windmask[ix] = True

np.save('../../Data/Metadata/lats_COSMO.npy', lats)
np.save('../../Data/Metadata/lons_COSMO.npy', lons)
np.save('../../Data/Metadata/onshore_COSMO.npy', onshore)
np.save('../../Data/Metadata/windmask_COSMO.npy', windmask)
np.save('../../Data/Metadata/solarmask_COSMO.npy', solarmask)
