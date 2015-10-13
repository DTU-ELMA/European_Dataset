import numpy as np
import scipy.sparse as sparse
import argparse, os
from itertools import izip as zip

# Uses the output of nodal_projection_matrix.py to aggregate signals
# into the nodal domain.

parser = argparse.ArgumentParser(description='Wind conversion options')
parser.add_argument('-r', '--indir', help='Input directory for forecast files', default='../../Data/Signal_Converted', metavar="load root")
parser.add_argument('-o', '--outdir', help='Output directory for forecast files', default='../../Data/Nodal_Signal', metavar="load outroot")
parser.add_argument('-f', '--first', help='First year to extract', default=2012, type=int, metavar="first year")
parser.add_argument('-l', '--last', help='Last year to extract', default=2014, type=int, metavar="last year")
parser.add_argument('-fm', help='First month to extract', default=1, type=int, metavar="first month")
parser.add_argument('-lm', help='Last month to extract', default=12, type=int, metavar="last month")

args = parser.parse_args()

loadtransfer = np.load('../../Data/Metadata/loadtransfercsr_ECMWF.npz')
loadtransfer = sparse.csr_matrix((loadtransfer['data'], loadtransfer['indices'], loadtransfer['indptr']), shape=loadtransfer['shape'])

loadname = 'load-{0:04d}{1:02d}.npz'

indirls = sorted(os.listdir(args.indir))

loadls = [x for x in indirls if 'load-' in x]

startidx = loadls.index(loadname.format(args.first, args.fm))

try:
    stopidx = loadls.index(loadname.format(args.last+int(args.lm == 12), args.lm % 12+1))
    loadls = loadls[startidx:stopidx]
except ValueError:
    print 'Stopdate + 1 month not found - assuming we need to use all directories'
    loadls = loadls[startidx:]

for loadfile in loadls:
    print loadfile
    dataf = np.load(args.indir + '/' + loadfile)
    dates = dataf['dates']
    data = dataf['data']
    shape = data.shape
    outdata = loadtransfer.dot(np.reshape(data, (shape[0], shape[1]*shape[2])).T).T
    np.savez_compressed(args.outdir + '/' + loadfile, data=outdata, dates=dates)
