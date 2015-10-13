import numpy as np
import pandas as pd
import os

instore = '../../Data/Nodal_Power/COSMO-store.h5'
outdir = '../../Output_Data/Nodal_TS/'

store = pd.HDFStore(instore)

winddf = store['COSMO/wind']

print 'Loaded wind'

solardf = store['COSMO/solar']

print 'Loaded solar'

winddf = winddf[winddf.index < pd.Timestamp('2015-01-01 00:00:00')]
solardf = solardf[solardf.index < pd.Timestamp('2015-01-01 00:00:00')]

winddf.index.name = 'Time'
solardf.index.name = 'Time'

winddf.columns = map(int, winddf.columns)
solardf.columns = map(int, solardf.columns)

winddf.to_csv(outdir + 'wind_signal_COSMO.csv', float_format='%.4f')
solardf.to_csv(outdir + 'solar_signal_COSMO.csv', float_format='%.4f')
