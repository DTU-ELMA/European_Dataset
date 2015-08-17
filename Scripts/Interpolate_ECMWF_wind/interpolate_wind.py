import numpy as np
from EOF_interp import do_EOF_interpolation
import os

indir = '../../Data/Signal_Unprocessed/'
outdir = '../../Data/Signal_Processed/'

# Get fields to interpolate
directory = os.listdir(indir)
directory = sorted([x for x in directory if ('wnduv10m' in x) or ('wnduv100m' in x)])

odir = os.listdir(outdir)
# Do not re-interpolate existing files
directory = [x for x in directory if x.replace('wnduv10', 'wnd10') not in odir]

for filename in directory:
    print filename
    rwnd = np.load(indir + filename)
    rwnd, dates = rwnd['data'], rwnd['dates']
    fullindx = range(len(rwnd))
    # Interpolate across 1 hr
    cutindx = [0] + [i for i in fullindx if (i) % 12 > 0]
    # Interpolate across 2 hrs
    # cutindx = [0] + [i for i in fullindx if (i-1) % 12 <= 9] + fullindx[-1:]
    iwnd = do_EOF_interpolation(rwnd, cutindx, fullindx)
    iwnd = np.sqrt(np.sum(iwnd**2, axis=1))
    np.savez(outdir + filename.replace('wnduv10', 'wnd10'), data=iwnd, dates=dates)
