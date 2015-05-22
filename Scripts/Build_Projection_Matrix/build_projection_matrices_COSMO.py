import numpy as np
import networkx as nx
from latlon_to_spatial import latlonstospace
from scipy.spatial import KDTree
import scipy.sparse as sparse

nodeorder = np.load('../../Data/Metadata/nodeorder.npy')
windmask = np.load('../../Data/Metadata/windmask_COSMO.npy').astype(bool)
solarmask = np.load('../../Data/Metadata/solarmask_COSMO.npy').astype(bool)
lats = np.load('../../Data/Metadata/lats_COSMO.npy')
lons = np.load('../../Data/Metadata/lons_COSMO.npy')


windgridpos = np.array([lons[windmask], lats[windmask]]).T
windgridspos = latlonstospace(windgridpos[:, 1], windgridpos[:, 0])

solargridpos = np.array([lons[solarmask], lats[solarmask]]).T
solargridspos = latlonstospace(solargridpos[:, 1], solargridpos[:, 0])

# ENTSOE grid data
entsoe_grid = nx.read_gpickle('../../Data/Metadata/network_postfit.gpickle')
nodepos = nx.get_node_attributes(entsoe_grid, 'pos')
nodepos = np.array([nodepos[n] for n in nodeorder])
nodespos = latlonstospace(nodepos[:, 1], nodepos[:, 0])


# Construct KDTrees for fast lookup
nodetree = KDTree(nodespos)
windgridtree = KDTree(windgridspos)
solargridtree = KDTree(solargridspos)

# # # WIND and LOAD transfer matrix contruction

wndtransferbig = sparse.lil_matrix((len(nodeorder), len(lats.flatten())))

dummy, windx = nodetree.query(windgridspos)
dummy, windy = windgridtree.query(nodespos)

windxindx = np.argwhere(windmask.flatten())

# Each gridpoint in mask gets assigned to a node
for i, j in zip(windx, range(len(windx))):
    wndtransferbig[i, windxindx[j]] = 1.

# Each node gets assigned to a gridpoint (avoids some nodes ending up without a signal)
for j, i in zip(windy, range(len(windy))):
    wndtransferbig[i, windxindx[j]] = 1.

# # Normalization step
# Make sure each gridpoint is divided evenly among associated nodes
ssum = np.squeeze(np.asarray(wndtransferbig.sum(0)))
nindx, sindx = wndtransferbig.nonzero()
for i, j in zip(nindx, sindx):
    wndtransferbig[i, j] /= ssum[j]


# # LOAD transfer matrix should preserve sum of incoming squares.
loadtransferout = wndtransferbig.tocsr()
np.savez('../../Data/Metadata/loadtransfercsr_COSMO.npz', data=loadtransferout.data, indices=loadtransferout.indices, indptr=loadtransferout.indptr, shape=loadtransferout.shape)


# Make sure each node gets an average over the available area's capacity factor.
nsum = np.squeeze(np.asarray(wndtransferbig.sum(1)))
for i, j in zip(nindx, sindx):
    wndtransferbig[i, j] /= nsum[i]

# # Wind tansfer matrix should preserve average of incoming squares.
wndtransferout = wndtransferbig.tocsr()

np.savez('../../Data/Metadata/wndtransfercsr_COSMO.npz', data=wndtransferout.data, indices=wndtransferout.indices, indptr=wndtransferout.indptr, shape=wndtransferout.shape)

# to load:
# wndtransfer = np.load('metadata/wndtransfercsr.npz')
# wndtransfer = sparse.csr_matrix((wndtransfer['data'], wndtransfer['indices'], wndtransfer['indptr']), shape=wndtransfer['shape'])


# # # # SOLAR transfer matrix contruction
solartransferbig = sparse.lil_matrix((len(nodeorder), len(lats.flatten())))

dummy, solarx = nodetree.query(solargridspos)
dummy, solary = solargridtree.query(nodespos)

solarindx = np.argwhere(solarmask.flatten())

# Each gridpoint in mask gets assigned to a node
for i, j in zip(solarx, range(len(solarx))):
    solartransferbig[i, solarindx[j]] = 1.

# Each node gets assigned to a gridpoint (avoids some nodes ending up without a signal)
for j, i in zip(solary, range(len(solary))):
    solartransferbig[i, solarindx[j]] = 1.


# # Normalization step
# Make sure each gridpoint is divided evenly among associated nodes
ssum = np.squeeze(np.asarray(solartransferbig.sum(0)))
nindx, sindx = solartransferbig.nonzero()
for i, j in zip(nindx, sindx):
    solartransferbig[i, j] /= ssum[j]

# # Comment out to preserve sum of the incoming vector!
# Make sure each node gets an average over the available area's capacity factor.
nsum = np.squeeze(np.asarray(solartransferbig.sum(1)))
for i, j in zip(nindx, sindx):
    solartransferbig[i, j] /= nsum[i]

solartransferout = solartransferbig.tocsr()

np.savez('../../Data/Metadata/solartransfercsr_COSMO.npz', data=solartransferout.data, indices=solartransferout.indices, indptr=solartransferout.indptr, shape=solartransferout.shape)

# to load:
# solartransfer = np.load('metadata/solartransfercsr.npz')
# solartransfer = sparse.csr_matrix((solartransfer['data'], solartransfer['indices'], solartransfer['indptr']), shape=solartransfer['shape'])
