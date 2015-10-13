import networkx as nx
import numpy as np
import pickle
from scipy.spatial import KDTree
from latlon_to_spatial import latlonstospace

datadir = '../../Data/'
metadatadir = datadir + 'Metadata/'
nodeorder = np.load(metadatadir + 'nodeorder.npy')

generators = pickle.load(open(metadatadir + 'generator_database_no_affiliation.pickle'))
entsoe_grid = nx.read_gpickle(metadatadir + 'network_postfit.gpickle')
nodepos = nx.get_node_attributes(entsoe_grid, 'pos')
nodelatlon = np.array([nodepos[n] for n in nodeorder])
nodespos = latlonstospace(nodelatlon[:, 1], nodelatlon[:, 0])

# Fast lookup of node position
nodetree = KDTree(nodespos)

generatororder = generators.keys()
generatorlatlon = np.array([generators[g]['location'] for g in generatororder])
generatorspos = latlonstospace(generatorlatlon[:, 1], generatorlatlon[:, 0])
distances, nodeidx = nodetree.query(generatorspos)
for gen, n in zip(generators, nodeorder[nodeidx]):
	generators[gen]['origin'] = n


pickle.dump(generators, open(metadatadir + 'generator_database_affiliation.pickle', 'w'))
