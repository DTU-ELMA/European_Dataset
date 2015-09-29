import numpy as np
import os
import datetime
import argparse
import Myhelpers.defaults as defaults
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pygrib as pg
import scipy.sparse as sparse

from windconversionfunctions_cosmo import convertWind
from configobj import ConfigObj
from validate import Validator
from itertools import izip as zip
from Myhelpers import write_datetime_string, parse_datetime_string

# Argument parser
parser = argparse.ArgumentParser(description='Wind conversion options')

parser.add_argument('-r', '--rootdir', help='Input directory for wind files', default=defaults.winddatadir, metavar="wind root")
parser.add_argument('-o', '--outdir', help='Output directory for wind files', default=defaults.windoutdir, metavar="wind outroot")

parser.add_argument('-f', '--first', help='First year to extract', default=defaults.startyear, type=int, metavar="first year")
parser.add_argument('-l', '--last', help='Last year to extract', default=defaults.endyear, type=int, metavar="last year")
parser.add_argument('-fm', help='First month to extract', default=defaults.startmonth, type=int, metavar="first month")
parser.add_argument('-lm', help='Last month to extract', default=defaults.endmonth, type=int, metavar="last month")
parser.add_argument('-onm', '--onshoremap', metavar="onshoremap", type=str, help='Numpy file containing the onshore map', default=defaults.onshoremapfilename)
parser.add_argument('-onc', '--onshoreconf', metavar="onshore_config_file", nargs=1, type=str, help='File containing characteristics of the onshore wind turbine to use', default=defaults.onshoreturbinecfg)
parser.add_argument('-ofc', '--offshoreconf', metavar="offshore_config_file", nargs=1, type=str, help='File containing characteristics of the offshore wind turbine to use', default=defaults.offshoreturbinecfg)
parser.add_argument('-md', '--halfheightfile', help='Half-height layers file', default=defaults.halfheightfile, type=str, metavar="halfheightfile")

args = parser.parse_args()

onshoremap = np.load(args.onshoremap)


class Constant_Height_Interpolator:

    def __init__(self, heights, single_level):
        self.upper_mask = np.pad(np.diff(heights > single_level, axis=0), ((0, 1), (0, 0), (0, 0)), mode='constant', constant_values=False)
        self.lower_mask = np.pad(np.diff(heights > single_level, axis=0), ((1, 0), (0, 0), (0, 0)), mode='constant', constant_values=False)
        x1 = self._collapse_mask(heights, self.lower_mask)
        x2 = self._collapse_mask(heights, self.upper_mask)
        self.c = (single_level-x1)/(x2-x1)
        self.d1 = np.log(single_level/x1)/np.log(x2/x1)
        self.d2 = np.log(single_level/x2)/np.log(x2/x1)
        self.x1 = x1
        self.x2 = x2

    def interpolate_field_linear(self, x):
        '''
            Linearly interpolate field x to the single level given on construction.
        '''
        return self.c*self._collapse_mask(x, self.upper_mask) + (1-self.c)*self._collapse_mask(x, self.lower_mask)

    def interpolate_field_logarithmic(self, x):
        return self.d1*self._collapse_mask(x, self.upper_mask) - self.d2*self._collapse_mask(x, self.lower_mask)            

    def _collapse_mask(self, x, m):
        '''
            given a 3d array x and a 3d mask m, multiplies x by m and sums along first axis.
        '''
        return np.einsum('ijk,ijk -> jk', x, m)


# Initialize turbine configurations
configspec = ConfigObj(
    "TurbineconfigLayout.cfg",
    list_values=True, file_error=True, _inspec=True)

onshoreturbine = ConfigObj(
    args.onshoreconf,
    list_values=True,
    configspec=configspec)
onshoreturbine.validate(Validator())

offshoreturbine = ConfigObj(
    args.offshoreconf,
    list_values=True,
    configspec=configspec)
offshoreturbine.validate(Validator())


# Set up filename
filename = "WNDpower_onshore-%s_offshore-%s" % (onshoreturbine['name'], offshoreturbine['name'])
filename = filename.replace(" ", "_")

# Load matrix to project to nodal space
wndtransfer = np.load(defaults.windprojectionmatrix)
wndtransfer = sparse.csr_matrix((wndtransfer['data'], wndtransfer['indices'], wndtransfer['indptr']), shape=wndtransfer['shape'])

# load nodeorder file (used for saving)
nodeorder = np.load(defaults.nodeorder)

hub_height_on = onshoreturbine['H']
hub_height_off = offshoreturbine['H']

# Open half-height model levels file
fH = pg.open(args.halfheightfile)

heights = np.array([x.values for x in fH])
lats, lons = x.latlons()

fdir = sorted(os.listdir(args.rootdir))

startdate = 'laf{0:04d}{1:02d}01000000'.format(args.first, args.fm)
stopdate = 'laf{0:04d}{1:02d}01000000'.format(args.last+int(args.lm == 12), args.lm % 12 + 1)

try:
    startidx = fdir.index(startdate)
except ValueError:
    print('Start month not found - check forecast directory')
    raise ValueError
try:
    stopidx = fdir.index(stopdate)
    fdir = fdir[startidx:stopidx]
except ValueError:
    print 'Stopmonth+1 not found - assuming we need to use all directories'
    fdir = fdir[startidx:]


converted_series = []
times = []
# wmean = 0
# i = 1
for cosmo_file in (x for x in fdir if x[0] != "."):

    print cosmo_file

    date = parse_datetime_string(cosmo_file)

    with pg.open(args.rootdir + cosmo_file) as f:
        d = [x for x in f]
        u = np.array([x.values for x in d[:6]])
        v = np.array([x.values for x in d[6:12]])
        w = np.sqrt(u**2 + v**2)
        # Some fields are malformed - cut away border from these fields
        if w[0].shape != lats.shape:
            flats, flons = d[0].latlons()
            latdev = (flats[16:-16, 16:-16] - lats).max()
            londev = (flons[16:-16, 16:-16] - lons).max()
            print "Found malformed wind fields at {0}, latdev = {1:.03f}, londev = {2:.03f}".format(date, latdev, londev)
            if latdev > 0.1 or londev > 0.1:
                raise ValueError("Malformed fields outside lat/lon tolerance")
            w = w[:, 16:-16, 16:-16]

        # Winds are sampled from the middle of model layers. Grib indexes from 1.
        windheights = np.array([(heights[x['bottomLevel']-1]+heights[x['topLevel']-1] - 2*heights[-1])/2 for x in d[:6]])

    # Build interpolators for onshore\offshore wind turbine
    inter_on = Constant_Height_Interpolator(windheights, hub_height_on)
    inter_off = Constant_Height_Interpolator(windheights, hub_height_off)

    # Interpolate to hub height
    out_windS_on = inter_on.interpolate_field_linear(w)
    out_windS_off = inter_on.interpolate_field_linear(w)

    out_windS = out_windS_on*onshoremap + out_windS_off*(1 - onshoremap)

    # Sanity check code.
    # wmean = ((i-1)*out_windS + wmean)/i
    # i += 1

    out = convertWind(onshoreturbine, offshoreturbine, out_windS, onshoremap)

    # idx = range(len(convdata))
    out[np.isnan(out)] = 0.0
    out[onshoremap] /= max(onshoreturbine['POW'])
    out[np.logical_not(onshoremap)] /= max(offshoreturbine['POW'])

    # Projection to nodal domain
    shape = out.shape
    outdata = wndtransfer.dot((out.flatten()).T).T

    converted_series.append(outdata)
    times.append(date)

# Store using HDF5 for fast loading.
outdf = pd.DataFrame(data=converted_series, index=times, columns=nodeorder)
store = pd.HDFStore(defaults.windoutdir + 'COSMO-store.h5')
try:
    olddf = store['COSMO/wind']
    store['COSMO/wind'] = outdf.combine_first(olddf)
except KeyError:
    store['COSMO/wind'] = outdf
store.close()
