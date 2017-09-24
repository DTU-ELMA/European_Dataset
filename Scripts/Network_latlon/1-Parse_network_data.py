import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


nodefile = 'buses.csv'
linkfile = 'lines.csv'

G=nx.Graph()
nodeset=set()
with open(nodefile) as afile:
	afile.readline() #Clear first row
	for line in afile:
		name,x,y,realname,voltage = line.split('\t')
		G.add_node(name,pos=np.array([float(x),float(y)]),name=realname,voltage=int(voltage))
		nodeset.add(name)

with open(linkfile) as afile:
	afile.readline() #Clear first row
	for line in afile:
		n1,n2,X,limit=line.split('\t')
		n2 = n2.rstrip()
		X,limit = float(X),float(limit)
		if (n1 in nodeset) and (n2 in nodeset):
			if G.has_edge(n1,n2):
				Xold = G[n1][n2]['X']
				limitold = G[n1][n2]['limit']
				Xnew = 1/(1./X+1./Xold)
                                numold = G[n1][n2]['num']
				G.add_edge(
                                        n1, n2,
                                        X = Xnew,
                                        limit = limit + limitold,
                                        num=numold+1)
			else:
				G.add_edge(n1,n2,X = X,limit = limit, num = 1)
		else:
			print "Unable to find nodes {0} and {1}!".format(n1,n2)

metadatadir = '../../Data/Metadata/'

nx.write_gpickle(G,metadatadir + 'network_prefit.gpickle')
