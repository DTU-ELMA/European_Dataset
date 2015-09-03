import numpy as np
import pandas as pd

metadatadir = '../../Data/Metadata/'

nodeorder = np.load(metadatadir + 'nodeorder.npy')

windarea = np.load(metadatadir + 'Node_area_wind_onshore_ECMWF.npy') + \
    np.load(metadatadir + 'Node_area_wind_offshore_ECMWF.npy')
solararea = np.load(metadatadir + 'Node_area_PV_ECMWF.npy')

wind = pd.read_csv('../../Output_Data/Nodal_TS/wind_signal_ECMWF.csv')
solar = pd.read_csv('../../Output_Data/Nodal_TS/solar_signal_ECMWF.csv')
load = pd.read_csv('../../Output_Data/Nodal_TS/load_signal.csv')

loadsum = load.set_index('Time').sum().sum()
windrelarea = windarea / np.sum(windarea)
solarrelarea = solararea / np.sum(solararea)

windsum = wind.set_index('Time').sum()[nodeorder].values
solarsum = solar.set_index('Time').sum()[nodeorder].values
windrelsum = windsum / windsum.sum()
solarrelsum = solarsum / solarsum.sum()

wind_layout_uniform = windrelarea * loadsum / (windrelarea * windsum).sum()
solar_layout_uniform = solarrelarea * loadsum / (solarrelarea * solarsum).sum()

wind_layout_proportional = windrelarea * windrelsum * loadsum / (windrelarea * windrelsum * windsum).sum()
solar_layout_proportional = solarrelarea * solarrelsum * loadsum / (solarrelarea * solarrelsum * solarsum).sum()

np.save(metadatadir + 'wind_layout_uniform_ECMWF.npy', wind_layout_uniform)
np.save(metadatadir + 'solar_layout_uniform_ECMWF.npy', solar_layout_uniform)
np.save(metadatadir + 'wind_layout_proportional_ECMWF.npy', wind_layout_proportional)
np.save(metadatadir + 'solar_layout_proportional_ECMWF.npy', solar_layout_proportional)
