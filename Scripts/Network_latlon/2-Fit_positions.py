import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import networkx as nx

metadatadir = '../../Data/Metadata/'

def to_fit(pin,pout,coeffs):
	pf = np.array([func(p,coeffs) for p in pin])
	return np.sum((pout-pf)**2)

def func(p,coeffs):
	a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9 = coeffs
	x,y = p
	xs = a0 + a1*x + a2*y + a3*x**2 + a4*y**2 + a5*x*y\
		 + a6*x**3 + a7*x**2*y + a8*x*y**2 + a9*y**3
	ys = b0 + b1*x + b2*y + b3*x**2 + b4*y**2 + b5*x*y\
		 + b6*x**3 + b7*x**2*y + b8*x*y**2 + b9*y**3
	return np.array([xs,ys])

coeffs0 = [41,1,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0,0]

data = np.loadtxt('coordinates-mercator.txt')
mappoints = data[:,0:2]
latlons = data[:,2:4]

to_opt = lambda z,x=mappoints,y=latlons: to_fit(x,y,z)

optimal = opt.minimize(to_opt, coeffs0, method='Powell', options={'maxfev':100000,'maxiter':50000})
opted = np.array([func(p,optimal['x']) for p in mappoints])

G = nx.read_gpickle(metadatadir + 'network_prefit.gpickle')
pos = nx.get_node_attributes(G,'pos')
fitpos = {k:func(v,optimal['x'])[::-1] for k,v in pos.iteritems()}
nx.set_node_attributes(G,'pos',fitpos)

countrydata = np.loadtxt('bus_countries.csv',dtype = str, delimiter = ',')
countrydict = {p[0]:p[1] for p in countrydata}

Xdict = nx.get_edge_attributes(G,'X')
Ydict = {k:1/v for k,v in Xdict.iteritems()}
nx.set_edge_attributes(G,'Y',Ydict)


nx.set_node_attributes(G,'country',countrydict)

nx.write_gpickle(G,metadatadir + 'network_postfit.gpickle')

