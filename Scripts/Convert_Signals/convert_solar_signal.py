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
    '''
    out = [x/3600 for x in np.diff(L, axis=0)]
    out.append(L[0]/3600)
    return np.array(out)


# Argument parser
parser = argparse.ArgumentParser(description='Wind conversion options')

parser.add_argument('-r', '--rootdir', help='Input directory for signal files', default=defaults.solarsignaldatadir, metavar="signal root")
parser.add_argument('-o', '--outdir', help='Output directory for signal files', default=defaults.solarsignaloutdir, metavar="signal outroot")

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

# Input file names
dsolarfilename = 'dswsfc-{}.npz'
usolarfilename = 'uswsfc-{}.npz'
tmp2mfilename = 'tmp2m-{}.npz'

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
outfilename = "PVpower_{0}.npz".format(panelconfig['name'])
outfilename.replace(" ", "_")
outfilename += "-{0:04d}{1:02d}.npz"

# Load matrix to project to nodal space
solartransfer = np.load(defaults.solarprojectionmatrix)
solartransfer = sparse.csr_matrix((solartransfer['data'], solartransfer['indices'], solartransfer['indptr']), shape=solartransfer['shape'])

# load nodeorder file (used for saving)
nodeorder = np.load(defaults.nodeorder)

# Select only the forecasts specified for conversion.
signalls = sorted(os.listdir(args.rootdir))
dswsfcls = [x for x in signalls if 'dswsfc' in x]
uswsfcls = [x for x in signalls if 'uswsfc' in x]
tmpls = [x for x in signalls if 'tmp2m' in x]

startdate = '{0:04d}{1:02d}'.format(args.first, args.fm)
stopdate = '{0:04d}{1:02d}'.format(args.last+int(args.lm == 12), args.lm % 12+1)
try:
    dsstartidx = dswsfcls.index(dsolarfilename.format(startdate))
    usstartidx = uswsfcls.index(usolarfilename.format(startdate))
    tmpstartidx = tmpls.index(tmp2mfilename.format(startdate))
except ValueError:
    print('Start month not found - check directory')
    raise ValueError
try:
    dsstopidx = dswsfcls.index(dsolarfilename.format(stopdate))
    usstopidx = uswsfcls.index(usolarfilename.format(stopdate))
    tmpstopidx = tmpls.index(tmp2mfilename.format(stopdate))
    dswsfcls = dswsfcls[dsstartidx:dsstopidx]
    uswsfcls = uswsfcls[usstartidx:usstopidx]
    tmpls = tmpls[tmpstartidx:tmpstopidx]
except ValueError:
    print 'Stopdate + 1 month not found - assuming we need to use all time series'
    dswsfcls = dswsfcls[dsstartidx:]
    uswsfcls = uswsfcls[usstartidx:]
    tmpls = tmpls[tmpstartidx:]

# MAIN LOOP
# For each forecast:
# - Load fields of downward radiation, upward radiation and temperature
# - Convert to capacity factors
# - Project to nodal domain
# - Save nodal forecast time series
for dsolarfile, usolarfile, tmp2mfile in zip(dswsfcls, uswsfcls, tmpls):
    print dsolarfile
    dsfile = np.load(args.rootdir + '/' + dsolarfile)
    usfile = np.load(args.rootdir + '/' + usolarfile)
    tmpfile = np.load(args.rootdir + '/' + tmp2mfile)
    dsdata = dsfile['data']
    usdata = usfile['data']
    tmpdata = tmpfile['data']
    dates = dsfile['dates']
    convdata = np.zeros_like(dsdata)
    for influx, outflux, tmp2m, utcTime, outidx in zip(dsdata, usdata, tmpdata, dates, range(len(convdata))):
        influx_tilted = newHayDavies(influx, outflux, lats, lons, utcTime, slopefunction)
        out = SolarPVConversion((influx_tilted, tmp2m), panelconfig)
        out /= (panelconfig['rated_production']/panelconfig['area'])
        convdata[outidx] = np.nan_to_num(out)
    shape = convdata.shape
    outdata = solartransfer.dot(np.reshape(convdata, (shape[0], shape[1]*shape[2])).T).T

    np.savez_compressed(args.outdir + '/' + outfilename.format(dates[0].year, dates[0].month), data=outdata, dates=dates)
