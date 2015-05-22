# import numpy as np
import os
import pygrib as pg
import numpy as np
import argparse
import Myhelpers.defaults as defaults
import scipy.sparse as sparse

from solarconversionfunctions_cosmo import SolarPVConversion, newHayDavies, testSlopeFunction, fullTrackingSlopeFunction
from configobj import ConfigObj
from validate import Validator
from itertools import izip as zip
from Myhelpers import write_datetime_string, parse_datetime_string
from datetime import timedelta

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

fH = pg.open('metadata/HHL.grb')

lats, lons = fH[1].latlons()

# Select only the forecasts specified for conversion.
fdir = sorted(os.listdir(args.rootdir))

startdate = '{0:04d}{1:02d}0100'.format(args.first, args.fm)
stopdate = '{0:04d}{1:02d}0100'.format(args.last+int(args.lm == 12), args.lm % 12 + 1)

# try:
#     startidx = forecastls.index(startdate)
# except ValueError:
#     print('Start month not found - check forecast directory')
#     raise ValueError
# try:
#     stopidx = forecastls.index(stopdate)
#     forecastls = forecastls[startidx:stopidx]
# except ValueError:
#     print 'Stopmonth+1 not found - assuming we need to use all directories'
#     forecastls = forecastls[startidx:]

# MAIN LOOP
# For each forecast:
# - Extract fields of downward radiation, albedo and temperature
# - Calculate upward radiation
# - Convert to capacity factors
# - Project to nodal domain
# - Save nodal forecast time series

albold =0
tmpold = 0
Ibold = 0
Idold = 0
Igold = 0

for cosmo_file in (x for x in fdir if x[0] != "."):

    print cosmo_file

    date = parse_datetime_string(cosmo_file)
    previous = date + timedelta(hours = -1)

    hour = previous.hour

    # Load file
    f = pg.open(args.rootdir + cosmo_file)
    d = [x.values for x in f]
    alb = np.array(d[13]*(hour%6+1) - albold*(hour%6)).clip(0)
    tmp = np.array(d[14]*(hour%6+1) - tmpold*(hour%6)).clip(0)
    Ib = np.array(d[17]*(hour%6+1) - Ibold*(hour%6)).clip(0)
    Id = np.array(d[18]*(hour%6+1) - Idold*(hour%6)).clip(0)
    Ig = np.array(d[19]*(hour%6+1) - Igold*(hour%6)).clip(0)

    albold = d[13]
    tmpold = d[14]
    Ibold = d[17]
    Idold = d[18]
    Igold = d[19]

    # dsfile = pg.open(args.rootdir + fdir + '/' + dsrname)
    # albfile = pg.open(args.rootdir + fdir + '/' + albname)
    # tmpfile = pg.open(args.rootdir + fdir + '/' + tmpname)
    # dsdata_int = np.array([ds['values'] for ds in dsfile])
    # albdata = np.array([alb['values'] for alb in albfile])
    # tmpdata = np.array([tmp['values'] for tmp in tmpfile])
    # dsdata_int = np.array([ds['values'][::-1] for ds in dsfile])
    # albdata = np.array([alb['values'][::-1] for alb in albfile])
    # tmpdata = np.array([tmp['values'][::-1] for tmp in tmpfile])

    #dsdata = fix_solar(dsdata_int)
    #usdata = dsdata * albdata

    #dates = [date + forecastdelta*i for i in range(len(dsdata))]

    # solar conversion
    #convdata = np.zeros_like(dsdata)

    #influx, outflux, tmp2m, utcTime, outidx = dsdata, usdata, tmpdata, dates, range(len(convdata)))
    influx_tilted = newHayDavies(Ib, Id, Ig, lats, lons, date, slopefunction)
    out = SolarPVConversion((influx_tilted, tmp), panelconfig)
    out /= (panelconfig['rated_production']/panelconfig['area'])

    #convdata[outidx] = np.nan_to_num(out)

    # Projection to nodal domain
    shape = out.shape
    outdata = solartransfer.dot((out.flatten()).T).T

    # Save .npy file
    try:
        np.savez_compressed(args.outdir + '/' + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '_' + str(date.hour) + '_' + filename, data=outdata, dates=date)
    except IOError:
        os.mkdir(args.outdir + '/')
        np.savez_compressed(args.outdir + '/' + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '_' + str(date.hour) + '_' + filename, data=outdata, dates=date)
