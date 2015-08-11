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

parser.add_argument('-r', '--rootdir', help='Input directory for forecast files', default=defaults.windforecastdatadir, metavar="forecast root")
parser.add_argument('-o', '--outdir', help='Output directory for forecast files', default=defaults.windforecastoutdir, metavar="forecast outroot")

parser.add_argument('-f', '--first', help='First year to extract', default=defaults.startyear, type=int, metavar="first year")
parser.add_argument('-l', '--last', help='Last year to extract', default=defaults.endyear, type=int, metavar="last year")
parser.add_argument('-fm', help='First month to extract', default=defaults.startmonth, type=int, metavar="first month")
parser.add_argument('-lm', help='Last month to extract', default=defaults.endmonth, type=int, metavar="last month")
parser.add_argument('-onm', '--onshoremap', metavar="onshoremap", type=str, help='Numpy file containing the onshore map', default=defaults.onshoremapfilename)
parser.add_argument('-onc', '--onshoreconf', metavar="onshore_config_file", nargs=1, type=str, help='File containing characteristics of the onshore wind turbine to use', default=defaults.onshoreturbinecfg)
parser.add_argument('-ofc', '--offshoreconf', metavar="offshore_config_file", nargs=1, type=str, help='File containing characteristics of the offshore wind turbine to use', default=defaults.offshoreturbinecfg)

args = parser.parse_args()

onshoremap = np.load(args.onshoremap)

# We have a forecast for each hour
forecastdelta = datetime.timedelta(hours=1)

uname = 'ctr_P165_LSFC'
vname = 'ctr_P166_LSFC'
u100name = 'ctr_P246_LSFC'
v100name = 'ctr_P247_LSFC'


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

# Select only the forecasts specified for conversion.
forecastls = sorted(os.listdir(args.rootdir))
startdate = '{0:04d}{1:02d}0100'.format(args.first, args.fm)
stopdate = '{0:04d}{1:02d}0100'.format(args.last+int(args.lm == 12), args.lm % 12 + 1)
try:
    startidx = forecastls.index(startdate)
except ValueError:
    print('Start month not found - check forecast directory')
    raise ValueError
try:
    stopidx = forecastls.index(stopdate)
    forecastls = forecastls[startidx:stopidx]
except ValueError:
    print 'Stopmonth+1 not found - assuming we need to use all directories'
    forecastls = forecastls[startidx:]

# MAIN LOOP
# For each forecast:
# - Extract field of wind speeds
# - Convert to capacity factors
# - Project to nodal domain
# - Save nodal forecast time series
for fdir in forecastls:
    print fdir
    date = parse_datetime_string(fdir)

    # Load wind files
    ufile = pg.open(args.rootdir + fdir + '/' + uname)
    vfile = pg.open(args.rootdir + fdir + '/' + vname)
    # wlist = np.array([np.sqrt(u['values']**2 + v['values']**2) for u, v in zip(ufile, vfile)])
    wlist = np.array([np.sqrt(u['values']**2 + v['values']**2)[::-1] for u, v in zip(ufile, vfile)])
    u100file = pg.open(args.rootdir + fdir + '/' + u100name)
    v100file = pg.open(args.rootdir + fdir + '/' + v100name)
    # w100list = np.array([np.sqrt(u['values']**2 + v['values']**2) for u, v in zip(u100file, v100file)])
    w100list = np.array([np.sqrt(u['values']**2 + v['values']**2)[::-1] for u, v in zip(u100file, v100file)])

    dates = [date + forecastdelta*i for i in range(len(wlist))]

    # Wind conversion
    convdata = np.zeros_like(wlist)

    for wind, wind100m, date, outidx in zip(wlist, w100list, dates, range(len(convdata))):
        out = convertWind(onshoreturbine, offshoreturbine, wind, wind100m, onshoremap)
        out[np.isnan(out)] = 0.0
        out[onshoremap] /= max(onshoreturbine['POW'])
        out[np.logical_not(onshoremap)] /= max(offshoreturbine['POW'])
        convdata[outidx] = out

    # Projection to nodal domain
    shape = convdata.shape
    outdata = wndtransfer.dot(np.reshape(convdata, (shape[0], shape[1]*shape[2])).T).T

    # Save .npy file
    try:
        np.savez_compressed(args.outdir + '/' + fdir + '/' + filename, data=outdata, dates=dates)
    except IOError:
        os.mkdir(args.outdir + '/' + fdir + '/')
        np.savez_compressed(args.outdir + '/' + fdir + '/' + filename, data=outdata, dates=dates)
    if forecastls.index(fdir) > 10:
        raise SystemExit