import os
import numpy as np
from itertools import izip

regiondir = '../../Data/Metadata/Regions/'
indir = '../../Data/ENTSOE-load/extracted_load/'
outdir = '../../Data/Signal_Converted/'

convertyear = '2014'


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


popdens = np.load('../../Data/Metadata/popdens_ECMWF.npy')
countrylist = [x.split('_')[0] for x in os.listdir(indir) if convertyear in x]

dates = np.load('../../Data/Metadata/dates_' + convertyear + '.npy')


loads = [np.load(indir + x+'_' + convertyear + '.npy') for x in countrylist]
countrymasks = [np.load(regiondir + x + '.npy').astype(int) for x in countrylist]
countrymasks_onshore = [np.load(regiondir + x + '-onshore.npy').astype(int) for x in countrylist]

lats = np.load('../../Data/Metadata/lats_ECMWF.npy')
lons = np.load('../../Data/Metadata/lons_ECMWF.npy')

area = get_relative_area_of_cells(lats, lons)

pop = popdens * area

popmasks = [pop * mask for mask in countrymasks_onshore]
relpopmasks = np.array([pm/np.sum(pm) for pm in popmasks])

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
