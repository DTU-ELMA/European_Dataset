import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


nodefile = 'buses.csv'
linkfile = 'lines.csv'

G=nx.Graph()
nodeset=set()
with open(nodefile) as afile:
	#afile.readline() #Clear first row
	for line in afile:
		n,name,x,y = line.split(',')
		G.add_node(int(n),pos=np.array([float(x),float(y)]),name=name)
		nodeset.add(n)

with open(linkfile) as afile:
	#afile.readline() #Clear first row
	for line in afile:
		n1,n2,L,V=line.split(';')
		#n2 = n2.rstrip()
		L,V = float(L),float(V)
		if (n1 in nodeset) and (n2 in nodeset):
			if G.has_edge(n1,n2):
				Lold = G[n1][n2]['L'] 
				Vold = G[n1][n2]['V']
				Lnew = 1/(1./L+1./Lold)
				G.add_edge(int(n1),int(n2),L = Lnew,V = V + Vold)
			else:
				G.add_edge(int(n1),int(n2),L = L,V = V)
		else:
			print "Unable to find nodes {0} and {1}!".format(n1,n2)

metadatadir = 'Data/'

nx.write_gpickle(G,metadatadir + 'network_prefit.gpickle')
