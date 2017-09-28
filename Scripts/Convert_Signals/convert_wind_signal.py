import numpy as np
import os
import datetime
import pygrib as pg
import argparse
import Myhelpers.defaults as defaults
import scipy.sparse as sparse

from windconversionfunctions2 import convertWind
from configobj import ConfigObj
from validate import Validator
from itertools import izip as zip
from Myhelpers import write_datetime_string, parse_datetime_string

# Argument parser
parser = argparse.ArgumentParser(description='Wind conversion options')

parser.add_argument('-r', '--rootdir', help='Input directory for forecast files', default=defaults.windsignaldatadir, metavar="forecast root")
parser.add_argument('-o', '--outdir', help='Output directory for forecast files', default=defaults.windsignaloutdir, metavar="forecast outroot")

parser.add_argument('-f', '--first', help='First year to extract', default=defaults.startyear, type=int, metavar="first year")
parser.add_argument('-l', '--last', help='Last year to extract', default=defaults.endyear, type=int, metavar="last year")
parser.add_argument('-fm', help='First month to extract', default=defaults.startmonth, type=int, metavar="first month")
parser.add_argument('-lm', help='Last month to extract', default=defaults.endmonth, type=int, metavar="last month")
parser.add_argument('-onm', '--onshoremap', metavar="onshoremap", type=str, help='Numpy file containing the onshore map', default=defaults.onshoremapfilename)
parser.add_argument('-onc', '--onshoreconf', metavar="onshore_config_file", type=str, help='File containing characteristics of the onshore wind turbine to use', default=defaults.onshoreturbinecfg)
parser.add_argument('-ofc', '--offshoreconf', metavar="offshore_config_file", type=str, help='File containing characteristics of the offshore wind turbine to use', default=defaults.offshoreturbinecfg)

args = parser.parse_args()

print('Conversion arguments:')
print(args)

onshoremap = np.load(args.onshoremap)

# # We have a forecast for each hour
# forecastdelta = datetime.timedelta(hours=1)

# uname = 'ctr_P165_LSFC'
# vname = 'ctr_P166_LSFC'
# u100name = 'ctr_P246_LSFC'
# v100name = 'ctr_P247_LSFC'


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
outfilename = "WNDpower_onshore-%s_offshore-%s" % (onshoreturbine['name'], offshoreturbine['name'])
outfilename = outfilename.replace(" ", "_")
outfilename += "-{0:04d}{1:02d}.npz"

# Load matrix to project to nodal space
wndtransfer = np.load(defaults.windprojectionmatrix)
wndtransfer = sparse.csr_matrix((wndtransfer['data'], wndtransfer['indices'], wndtransfer['indptr']), shape=wndtransfer['shape'])

# load nodeorder file (used for saving)
nodeorder = np.load(defaults.nodeorder)

# Select only the months specified for conversion.
windls = sorted(os.listdir(args.rootdir))
windls = [x for x in windls if 'wnd10m' in x]
filename = 'wnd10m-{0:04d}{1:02d}.npz'
startdate = filename.format(args.first, args.fm)
stopdate = filename.format(args.last+int(args.lm == 12),args.lm % 12+1)
try:
    startidx = windls.index(startdate)
except ValueError:
    print('Start month not found - check directory')
    raise ValueError
try:
    stopidx = windls.index(stopdate)
    forecastls = windls[startidx:stopidx]
except ValueError:
    print 'Stopdate + 1 month not found - assuming we need to use all time series'
    forecastls = windls[startidx:]

# MAIN LOOP
# For each timestep:
# - Extract field of wind speeds
# - Convert to capacity factors
# - Project to nodal domain
# - Save time series
for windfile in windls:
    print windfile
    thefile = np.load(args.rootdir + '/' + windfile)
    the100mfile = np.load(args.rootdir + '/' + windfile.replace('wnd10m', 'wnd100m'))
    data = thefile['data']
    dates = thefile['dates']
    data100m = the100mfile['data']
    convdata = np.zeros_like(data)
    for wind, wind100m, date, outidx in zip(data, data100m, dates, range(len(convdata))):
        print date
        out = convertWind(onshoreturbine, offshoreturbine, wind, wind100m, onshoremap)
        out[np.isnan(out)] = 0.0
        out[onshoremap] /= max(onshoreturbine['POW'])
        out[np.logical_not(onshoremap)] /= max(offshoreturbine['POW'])
        convdata[outidx] = out
        shape = convdata.shape
    outdata = wndtransfer.dot(np.reshape(convdata, (shape[0], shape[1]*shape[2])).T).T
    np.savez(args.outdir + '/' + outfilename.format(dates[0].year, dates[0].month), data=outdata, dates=dates)
