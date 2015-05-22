import pygrib as pg
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import scipy.sparse as sparse

fH = pg.open('metadata/HHL.grb')
dH = [x for x in fH]

#heights = np.array([x.values for x in fH])
#lats, lons = x.latlons()

# heights = np.array([x.values for x in f])
# lats, lons = x.latlons()

# nodal = np.load('metadata/wndtransfercsr.npz')
# transfer = sparse.csr_matrix((nodal['data'], nodal['indices'], nodal['indptr']), shape=solartransfer['shape'])


# data = nodal['data']
# indices = nodal['indices']
# indptr = nodal['indptr']

# lats,lons = fH[1].latlons()
# # data = f2[1].values

# newlats = []
# newlons = []
# for i in range(0, len(lats)-1):
# 	newlats.append(lats[i])
# 	newlons.append(lons[i])

olats = np.load('../../Data/Metadata/lats.npy')
olons = np.load('../../Data/Metadata/lons.npy')
onshoremap = np.load('../../Data/Metadata/onshore.npy')

ndata = np.load('../../Data/Metadata/onshore_COSMO.npz')
nlats = ndata['lats']
nlons = ndata['lons']
nonshoremap = ndata['onshore']

# plt.contourf(lons, lats, data, 50, cmap=plt.cm.YlGnBu_r)
# plt.colorbar()
#plt.scatter(newlons, newlats)
plt.contourf(olons, olats, onshoremap, l=2)
plt.contourf(nlons, nlats, nonshoremap, l=2)
plt.tight_layout()
plt.show()

