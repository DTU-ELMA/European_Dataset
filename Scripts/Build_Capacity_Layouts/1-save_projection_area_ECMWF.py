import numpy as np
import scipy.sparse as sparse
from itertools import izip as zip

# Uses the output of nodal_projection_matrix.py to aggregate signals
# into the nodal domain.


def calc_rel_area_of_grid(lats, lons):
    Dlons = np.diff(np.deg2rad(lons), axis=1)
    Dlats = -np.diff(np.sin(np.deg2rad(lats)), axis=0)
    Dlons = np.pad(Dlons, ((0, 0), (0, 1)), 'edge')
    Dlats = np.pad(Dlats, ((0, 1), (0, 0)), 'edge')
    Rearth = 6371
    area = Dlons * Dlats * Rearth**2
    return area

lats = np.load('../../Data/Metadata/lats_ECMWF.npy')
lons = np.load('../../Data/Metadata/lons_ECMWF.npy')


wndtransfer = np.load('../../Data/Metadata/wndtransfercsr_ECMWF.npz')
wndtransfer = sparse.csr_matrix((wndtransfer['data']/wndtransfer['data'], wndtransfer['indices'], wndtransfer['indptr']), shape=wndtransfer['shape'])

solartransfer = np.load('../../Data/Metadata/solartransfercsr_ECMWF.npz')
solartransfer = sparse.csr_matrix((solartransfer['data']/solartransfer['data'], solartransfer['indices'], solartransfer['indptr']), shape=solartransfer['shape'])

onshore = np.load('../../Data/Metadata/onshore_ECMWF.npy')

area = calc_rel_area_of_grid(lats, lons)

wndareaon = wndtransfer.dot((area*onshore).flatten())
wndareaoff = wndtransfer.dot((area*(1-onshore)).flatten())
solarareaon = solartransfer.dot((area*onshore).flatten())

np.save('../../Data/Metadata/Node_area_wind_onshore_ECMWF.npy', wndareaon)
np.save('../../Data/Metadata/Node_area_wind_offshore_ECMWF.npy', wndareaoff)
np.save('../../Data/Metadata/Node_area_PV_ECMWF.npy', solarareaon)
