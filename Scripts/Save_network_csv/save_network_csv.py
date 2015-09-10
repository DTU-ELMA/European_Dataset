import numpy as np
import networkx as nx
import pandas as pd
import pickle
from great_circle_distance import gcdistance

metadatadir = '../../Data/Metadata/'
outdir = '../../Output_Data/Metadata/'

G = nx.read_gpickle(metadatadir + 'network_postfit.gpickle')
nodeorder = np.load(metadatadir + 'nodeorder.npy')
edgeorder = np.load(metadatadir + 'edgeorder.npy')
noded = G.node
edged = G.edge
nodedf = pd.DataFrame(
    {
        'ID': [n for n in nodeorder],
        'country': [noded[n]['country'] for n in nodeorder],
        'name': [noded[n]['name'] for n in nodeorder],
        'longitude': [noded[n]['pos'][0] for n in nodeorder],
        'latitude': [noded[n]['pos'][1] for n in nodeorder],
        'voltage': [noded[n]['voltage'] for n in nodeorder]
    },
    index=range(len(nodeorder))
)
edgedf = pd.DataFrame(
    {
        'fromNode': [n1 for n1, n2 in edgeorder],
        'toNode': [n2 for n1, n2 in edgeorder],
        'limit': [edged[n1][n2]['limit'] for n1, n2 in edgeorder],
        'X': [edged[n1][n2]['X'] for n1, n2 in edgeorder],
        'Y': [edged[n1][n2]['Y'] for n1, n2 in edgeorder],
        'length': [gcdistance(noded[n1]['pos'][1], noded[n2]['pos'][1], noded[n1]['pos'][0], noded[n2]['pos'][0]) for n1, n2 in edgeorder]
    },
    index=range(len(edgeorder))
)

# write .csv files
nodedf.to_csv(
    outdir + 'network_nodes.csv',
    columns=['ID', 'name', 'country', 'voltage', 'latitude', 'longitude'],
    index=False,
    encoding='UTF-8'
)
edgedf.to_csv(
    outdir + 'network_edges.csv',
    columns=['fromNode', 'toNode', 'X', 'Y', 'limit', 'length'],
    index=False,
    encoding='UTF-8'
)

gen = pickle.load(open(metadatadir + 'generator_database_affiliation.pickle'))
genorder = np.load(metadatadir + 'generatororder.npy')
gendf = pd.DataFrame(
    {
        'ID': [g for g in genorder],
        'name': [gen[g]['name'] for g in genorder],
        'country': [gen[g]['country'] for g in genorder],
        'origin': [gen[g]['origin'] for g in genorder],
        'latitude': [gen[g]['location'][1] for g in genorder],
        'longitude': [gen[g]['location'][0] for g in genorder],
        'status': [gen[g]['status'] for g in genorder],
        'primaryfuel': [gen[g]['primaryfuel'] for g in genorder],
        'secondaryfuel': [gen[g]['secondaryfuel'] for g in genorder],
        'capacity': [gen[g]['capacity'] for g in genorder],
        'lincost': [gen[g]['lincost'] for g in genorder],
        'cyclecost': [gen[g]['cyclecost'] for g in genorder],
        'minuptime': [gen[g]['minuptime'] for g in genorder],
        'mindowntime': [gen[g]['mindowntime'] for g in genorder],
        'minonlinecapacity': [gen[g]['minonlinecapacity'] for g in genorder]
    }
)
gendf.to_csv(
    outdir + 'generator_info.csv',
    columns=['ID', 'name', 'country', 'origin', 'latitude', 'longitude', 'status', 'primaryfuel', 'secondaryfuel', 'capacity', 'lincost', 'cyclecost', 'minuptime', 'mindowntime', 'minonlinecapacity'],
    index=False,
    encoding='UTF-8'
)
