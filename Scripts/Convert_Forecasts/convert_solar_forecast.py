import numpy as np
import os
import datetime
import pygrib as pg
import argparse
import Myhelpers.defaults as defaults
import scipy.sparse as sparse

from solarconversionfunctions import SolarPVConversion, newHayDavies, testSlopeFunction, fullTrackingSlopeFunction
from configobj import ConfigObj
from validate import Validator
from itertools import izip as zip
from Myhelpers import write_datetime_string, parse_datetime_string


def fix_solar(L):
    '''
    Integrated field to hourly average values.
    Divides by 3600 to convert joule = watthr to watthr/hr.
    In a market context, the energy is assigned proactively to the following hour,
    while the integrated field reports the accumulation over the last hour,
    hence the appended 'measurement' should be at the end of the time series.
    '''
    out = [x/3600 for x in np.diff(L, axis=0)]
    out.append(L[0]/3600)
    return np.array(out)


# Argument parser
parser = argparse.ArgumentParser(description='Wind conversion options')

parser.add_argument('-r', '--rootdir', help='Input directory for forecast files', default=defaults.solarforecastdatadir, metavar="forecast root")
parser.add_argument('-o', '--outdir', help='Output directory for forecast files', default=defaults.solarforecastoutdir, metavar="forecast outroot")

parser.add_argument('-f', '--first', help='First year to extract', default=defaults.startyear, type=int, metavar="first year")
parser.add_argument('-l', '--last', help='Last year to extract', default=defaults.endyear, type=int, metavar="last year")
parser.add_argument('-fm', help='First month to extract', default=defaults.startmonth, type=int, metavar="first month")
parser.add_argument('-lm', help='Last month to extract', default=defaults.endmonth, type=int, metavar="last month")
parser.add_argument('-sp', '--solarpaneltypefile', metavar="solarpaneltypefile", type=str, help='File containing characteristics of the solar panel to use', default=defaults.solarpanelcfg)
parser.add_argument('-la', '--latfile', help='Latitude file', default=defaults.latitudefile, type=str, metavar="latfile")
parser.add_argument('-lo', '--lonfile', help='Longitude file', default=defaults.longitudefile, type=str, metavar="lonfile")

args = parser.parse_args()

lats = np.load(args.latfile)
lons = np.load(args.lonfile)

# We have a forecast for each hour
forecastdelta = datetime.timedelta(hours=1)

# Temperature, downward solar and Albedo name
tmpname = 'ctr_P167_LSFC'
dsrname = 'ctr_P169_LSFC'
albname = 'ctr_P243_LSFC'

# PV slope function:
# Panel angled at 30 deg from horizontal
slopefunction = testSlopeFunction

# Initialize panel configurations
configspec = ConfigObj(
    "PVconfigLayout.cfg",
    list_values=True,
    file_error=True,
    _inspec=True)
panelconfig = ConfigObj(args.solarpaneltypefile, list_values=False, configspec=configspec)
panelconfig.validate(Validator())

# Set up filename
filename = "PVpower_{0}.npz".format(panelconfig['name'])
filename.replace(" ", "_")

# Load matrix to project to nodal space
solartransfer = np.load(defaults.solarprojectionmatrix)
solartransfer = sparse.csr_matrix((solartransfer['data'], solartransfer['indices'], solartransfer['indptr']), shape=solartransfer['shape'])

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
# - Extract fields of downward radiation, albedo and temperature
# - Calculate upward radiation
# - Convert to capacity factors
# - Project to nodal domain
# - Save nodal forecast time series
for fdir in forecastls:
    print fdir
    date = parse_datetime_string(fdir)

    # Load files
    dsfile = pg.open(args.rootdir + fdir + '/' + dsrname)
    albfile = pg.open(args.rootdir + fdir + '/' + albname)
    tmpfile = pg.open(args.rootdir + fdir + '/' + tmpname)
    dsdata_int = np.array([ds['values'] for ds in dsfile])
    albdata = np.array([alb['values'] for alb in albfile])
    tmpdata = np.array([tmp['values'] for tmp in tmpfile])

    dsdata = fix_solar(dsdata_int)
    usdata = dsdata * albdata

    dates = [date + forecastdelta*i for i in range(len(dsdata))]

    # solar conversion
    convdata = np.zeros_like(dsdata)

    for influx, outflux, tmp2m, utcTime, outidx in zip(dsdata, usdata, tmpdata, dates, range(len(convdata))):
        influx_tilted = newHayDavies(influx, outflux, lats, lons, utcTime, slopefunction)
        out = SolarPVConversion((influx_tilted, tmp2m), panelconfig)
        out /= (panelconfig['rated_production']/panelconfig['area'])
        convdata[outidx] = np.nan_to_num(out)

    # Projection to nodal domain
    shape = convdata.shape
    outdata = solartransfer.dot(np.reshape(convdata, (shape[0], shape[1]*shape[2])).T).T

    # Save .npy file
    try:
        np.savez_compressed(args.outdir + '/' + fdir + '/' + filename, data=outdata, dates=dates)
    except IOError:
        os.mkdir(args.outdir + '/' + fdir + '/')
        np.savez_compressed(args.outdir + '/' + fdir + '/' + filename, data=outdata, dates=dates)
