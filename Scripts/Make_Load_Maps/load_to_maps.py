import os
import numpy as np
import pandas as pd
from itertools import izip



regiondir = '../../Data/Metadata/Regions/'
# indir = '../../Data/ENTSOE-load/extracted_load/' # Switched to OPSD data
outdir = '../../Data/Signal_Converted/'

convertyear = '2012'


def get_relative_area_of_cells(lats, lons):
    '''
        Given a grid, estimate the area of each grid cell
    '''
    lons, lats = np.deg2rad(np.unique(lons)), np.deg2rad(np.unique(lats))
    dlons, dlats = np.diff(lons), np.diff(np.sin(lats))
    dlons, dlats = np.interp(lons, lons[:-1] + dlons/2, dlons), np.interp(lats, lats[:-1] + dlats/2, dlats)
    Dlons, Dlats = np.meshgrid(dlons, dlats)
    areamap = Dlons*Dlats
    areamap /= np.mean(areamap)
    return areamap

# Prepare load data
countrylist = ['ALB', 'AUT', 'BEL', 'BGR', 'BIH', 'CHE',
        'CZE', 'DEU', 'DNK', 'ESP', 'FRA', 'GRC', 'HRV',
        'HUN', 'ITA', 'KOS', 'LUX', 'MKD', 'MNE', 'NLD',
        'POL', 'PRT', 'ROU', 'SRB', 'SVK', 'SVN']
load_csv = pd.read_csv('../../Data/OPSD-Load/opsd_load_data.csv', index_col=0)
loadsnip = load_csv.ix[[x for x in load_csv.index if x.startswith('2012-')]]
dates = np.load('../../Data/Metadata/dates_' + convertyear + '.npy')
loads = [loadsnip[x].values for x in countrylist]

# Map of population density + latitude and longitude of that map
popdens = np.load('../../Data/Metadata/popdens_ECMWF.npy')
lats = np.load('../../Data/Metadata/lats_ECMWF.npy')
lons = np.load('../../Data/Metadata/lons_ECMWF.npy')
area = get_relative_area_of_cells(lats, lons)
pop = popdens * area

# Scale population masks relative to total population
countrymasks = [np.load(regiondir + x + '.npy').astype(int) for x in countrylist]
countrymasks_onshore = [np.load(regiondir + x + '-onshore.npy').astype(int) for x in countrylist]
popmasks = [pop * mask for mask in countrymasks_onshore]
relpopmasks = np.array([pm/np.sum(pm) for pm in popmasks])

# Main loop:
# Project country time series according to relative population density
# Save maps per month for aggregation
loads2 = np.array(loads).T
lastmonth = dates[0].month
lastyear = dates[0].year
loadlist = []
loadtimes = []
for load, mydate in izip(loads2, dates):
    if mydate.hour == 0:
        print mydate
    curmonth = mydate.month
    curyear = mydate.year
    if not lastmonth == curmonth:
        np.savez_compressed(outdir + 'load-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz',data = loadlist, dates = loadtimes)
        loadlist = []
        loadtimes = []
        lastmonth = curmonth
        lastyear = curyear
    loadmap = np.einsum('ijk,i->jk', relpopmasks, load)
    loadlist.append(loadmap)
    loadtimes.append(mydate)

np.savez_compressed(outdir + 'load-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz',data = loadlist, dates = loadtimes)
