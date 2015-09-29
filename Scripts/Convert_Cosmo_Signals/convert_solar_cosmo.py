# import numpy as np
import os
import pygrib as pg
import numpy as np
import pandas as pd
import argparse
import Myhelpers.defaults as defaults
import scipy.sparse as sparse

from solarconversionfunctions_cosmo import SolarPVConversion, newHayDavies, testSlopeFunction, fullTrackingSlopeFunction
from configobj import ConfigObj
from validate import Validator
from itertools import izip as zip
from Myhelpers import write_datetime_string, parse_datetime_string
from datetime import timedelta


# Argument parser
parser = argparse.ArgumentParser(description='Wind conversion options')

parser.add_argument('-r', '--rootdir', help='Input directory for forecast files', default=defaults.solarforecastdatadir, metavar="forecast root")
parser.add_argument('-o', '--outdir', help='Output directory for forecast files', default=defaults.solarforecastoutdir, metavar="forecast outroot")

parser.add_argument('-f', '--first', help='First year to extract', default=defaults.startyear, type=int, metavar="first year")
parser.add_argument('-l', '--last', help='Last year to extract', default=defaults.endyear, type=int, metavar="last year")
parser.add_argument('-fm', help='First month to extract', default=defaults.startmonth, type=int, metavar="first month")
parser.add_argument('-lm', help='Last month to extract', default=defaults.endmonth, type=int, metavar="last month")
parser.add_argument('-sp', '--solarpaneltypefile', metavar="solarpaneltypefile", type=str, help='File containing characteristics of the solar panel to use', default=defaults.solarpanelcfg)
parser.add_argument('-md', '--halfheightfile', help='Half-height layers file', default=defaults.halfheightfile, type=str, metavar="halfheightfile")

args = parser.parse_args()

# lats = np.load(args.latfile)
# lons = np.load(args.lonfile)


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
filename = "PVpower_%s" % panelconfig['name']
filename.replace(" ", "_")

# Load matrix to project to nodal space
solartransfer = np.load(defaults.solarprojectionmatrix)
solartransfer = sparse.csr_matrix((solartransfer['data'], solartransfer['indices'], solartransfer['indptr']), shape=solartransfer['shape'])

# load nodeorder file (used for saving)
nodeorder = np.load(defaults.nodeorder)

# Load half-height data, latitude and longitude
fH = pg.open(args.halfheightfile)
lats, lons = fH[1].latlons()

# Select only the forecasts specified for conversion.
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

# MAIN LOOP
# For each forecast:
# - Extract fields of upward, downward, and ground reflected radiation and temperature
# - Convert to capacity factors
# - Project to nodal domain
# - Save nodal forecast time series

albold = 0
tmpold = 0
Ibold = 0
Idold = 0
Igold = 0

converted_series = []
times = []
for cosmo_file in (x for x in fdir if x[0] != "."):

    print cosmo_file

    date = parse_datetime_string(cosmo_file)
    previous = date + timedelta(hours=-1)

    hour = previous.hour

    # Load file
    with pg.open(args.rootdir + cosmo_file) as f:
        d = [x.values for x in f]
    # Albedo
    alb = np.array(d[13]*(hour % 6+1) - albold*(hour % 6)).clip(0)
    # Temperature
    tmp = np.array(d[14]*(hour % 6+1) - tmpold*(hour % 6)).clip(0)
    # Irradiation beam
    Ib = np.array(d[17]*(hour % 6+1) - Ibold*(hour % 6)).clip(0)
    # Irradiation diffuse
    Id = np.array(d[18]*(hour % 6+1) - Idold*(hour % 6)).clip(0)
    # Irradiation ground
    Ig = np.array(d[19]*(hour % 6+1) - Igold*(hour % 6)).clip(0)

    albold = d[13]
    tmpold = d[14]
    Ibold = d[17]
    Idold = d[18]
    Igold = d[19]

    # solar conversion
    influx_tilted = newHayDavies(Ib, Id, Ig, lats, lons, date, slopefunction)
    out = SolarPVConversion((influx_tilted, tmp), panelconfig)
    out /= (panelconfig['rated_production']/panelconfig['area'])

    # NaN's crop up for high latitudes in summer months
    # when the sun shines on the reverse face of the panel
    out = np.nan_to_num(out)

    # Projection to nodal domain
    shape = out.shape
    outdata = solartransfer.dot((out.flatten()).T).T

    converted_series.append(outdata)
    times.append(date)

outdf = pd.DataFrame(data=converted_series, index=times, columns=nodeorder)
store = pd.HDFStore(defaults.windoutdir + 'COSMO-store.h5')
try:
    olddf = store['COSMO/solar']
    store['COSMO/solar'] = outdf.combine_first(olddf)
except KeyError:
    store['COSMO/solar'] = outdf
store.close()
