import numpy as np
import os
import datetime
import pygrib as pg
from itertools import izip


def parse_datetime_string(s):
    y, m, d, h = int(s[:4]), int(s[4:6]), int(s[6:8]), int(s[8:10])
    return datetime.datetime(y, m, d, h)


def fix_solar(L):
    '''
    Integrated field to hourly average values.
    Divides by 3600 to convert joule per hour to watt.
    '''
    out = [L[0]/3600]
    out.extend([x/3600 for x in np.diff(L, axis=0)])
    return out


def unpack_2d_list(L):
    return [x for y in L for x in y]

# We have a forecast for each hour
forecastdelta = datetime.timedelta(0, 3600)

indir = '../../Data/ECMWF-data/'
# RT time series is saved here
outdirts = '../../Data/Signal_Unprocessed/'

uname = 'ctr_P165_LSFC'
vname = 'ctr_P166_LSFC'
u100name = 'ctr_P246_LSFC'
v100name = 'ctr_P247_LSFC'
tmpname = 'ctr_P167_LSFC'
dsrname = 'ctr_P169_LSFC'
albname = 'ctr_P243_LSFC'

wnduvname = 'wnduv10m'
wnduv100name = 'wnduv100m'
downsolarname = 'dswsfc'
upsolarname = 'uswsfc'
tmp2mname = 'tmp2m'

# Assume directory structure is raw_data/YYYYMMDDHH/fieldfile
# Fieldfile contains 90 hours of forecast data.
# Output is to fields/YYYYMMDDHH/fieldname.npz
# Output files are npz with:
# Data = TxMxN numpy array with the field values
# Time = T-length numpy array with the times, read from the directory structure.

directories = sorted(os.listdir(indir))

# Cut directories to extract from
directories = directories[directories.index('2014110100'):directories.index('2015010100')]

tswind, tswind100, tstimes = [], [], []
tsdsolar, tsusolar, tstmp = [], [], []

lastmonth = parse_datetime_string(directories[0]).month
lastyear = parse_datetime_string(directories[0]).year
for directory in directories:
    print directory
    date = parse_datetime_string(directory)

    # # Logic to handle ejecting sequential time series
    if not lastmonth == date.month:
        print 'Saving monthly time series {0:04d}{1:02d}'.format(lastyear, lastmonth)
        tswind = unpack_2d_list(tswind)
        tswind100 = unpack_2d_list(tswind100)
        tsdsolar = unpack_2d_list(tsdsolar)
        tsusolar = unpack_2d_list(tsusolar)
        tstmp = unpack_2d_list(tstmp)
        tstimes = unpack_2d_list(tstimes)

        lat, lon = ufile.message(1).latlons()

        np.savez_compressed(outdirts + '/' + wnduvname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tswind, dates=tstimes, lat=lat, lon=lon)
        np.savez_compressed(outdirts + '/' + wnduv100name + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tswind100, dates=tstimes, lat=lat, lon=lon)
        np.savez_compressed(outdirts + '/' + downsolarname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tsdsolar, dates=tstimes, lat=lat, lon=lon)
        np.savez_compressed(outdirts + '/' + upsolarname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tsusolar, dates=tstimes, lat=lat, lon=lon)
        np.savez_compressed(outdirts + '/' + tmp2mname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tstmp, dates=tstimes, lat=lat, lon=lon)

        tswind, tswind100, tsdsolar, tsusolar, tstmp, tstimes = [], [], [], [], [], []

        lastmonth = date.month
        lastyear = date.year

    ufile = pg.open(indir + directory + '/' + uname)
    vfile = pg.open(indir + directory + '/' + vname)
    uvlist = [(u['values'], v['values']) for u, v in izip(ufile, vfile)]

    u100file = pg.open(indir + directory + '/' + u100name)
    v100file = pg.open(indir + directory + '/' + v100name)
    uv100list = [(u['values'], v['values']) for u, v in izip(u100file, v100file)]

    dsolarfile = pg.open(indir + directory + '/' + dsrname)
    albedofile = pg.open(indir + directory + '/' + albname)
    tmpfile = pg.open(indir + directory + '/' + tmpname)

    dsolarlist = fix_solar([ds['values'] for ds in dsolarfile])
    albedolist = [a['values'] for a in albedofile]
    # # Upward solar radiation = downward solar * albedo
    usolarlist = [ds*a for ds, a in izip(dsolarlist, albedolist)]
    tmplist = [tmp['values'] for tmp in tmpfile]

    dates = [date + forecastdelta*i for i in range(len(uvlist))]

    tswind.append(uvlist[:12])
    tswind100.append(uv100list[:12])

    if date.hour == 00:
        tsdsolar.append(dsolarlist[:24])
        tsusolar.append(usolarlist[:24])
        tstmp.append(tmplist[:24])

    tstimes.append(dates[:12])


# Final save of sequential timeseries
print 'Saving monthly time series {0:04d}{1:02d}'.format(date.year, date.month)
tswind = unpack_2d_list(tswind)
tswind100 = unpack_2d_list(tswind100)
tsdsolar = unpack_2d_list(tsdsolar)
tsusolar = unpack_2d_list(tsusolar)
tstmp = unpack_2d_list(tstmp)
tstimes = unpack_2d_list(tstimes)

lat, lon = ufile.message(1).latlons()

np.savez_compressed(outdirts + '/' + wnduvname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tswind, dates=tstimes, lat=lat, lon=lon)
np.savez_compressed(outdirts + '/' + wnduv100name + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tswind100, dates=tstimes, lat=lat, lon=lon)
np.savez_compressed(outdirts + '/' + downsolarname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tsdsolar, dates=tstimes, lat=lat, lon=lon)
np.savez_compressed(outdirts + '/' + upsolarname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tsusolar, dates=tstimes, lat=lat, lon=lon)
np.savez_compressed(outdirts + '/' + tmp2mname + '-' + str(lastyear) + '{:02d}'.format(lastmonth) + '.npz', data=tstmp, dates=tstimes, lat=lat, lon=lon)
