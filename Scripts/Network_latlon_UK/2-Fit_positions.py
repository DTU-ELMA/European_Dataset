import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import networkx as nx

import math

metadatadir = 'Data/'

def fitpoly2d(x, y, z, order=1):
    '''
    Fit z = p(x,y) where p is a polynomial of the given order
    Input:
        x,y,z: Scalars or numpy arrays of length N.
        order: Polynomial order.
    Output:
        c: Array of coefficients.
    '''
    num_c = (order+1)*(order+2)/2
    X = np.ones(shape=(num_c, len(x)))
    for o in range(1, order+1):
        curoffset = o*(o+1)/2
        for i in range(o+1):
            X[curoffset+i] = x**i * y**(o-i)
    c = np.linalg.inv(X.dot(X.T)).dot(X.dot(z))
    return c
 
 
def calcpoly2d(x, y, c):
    '''
    Input:
        x,y: Input points to calculate. Scalars or numpy array of length n.
        c: Coefficients of the polynomial
    Output:
        out: Scalar or length-N array.
    '''
    order = int((np.sqrt(8*len(c)+1)-3)/2)
    out = np.zeros_like(x)
    for o in range(order+1):
        curoffset = o*(o+1)/2
        for i in range(o+1):
            out += c[curoffset+i] * x**i * y**(o-i)
    return out


def distance(lat1, lat2, lon1, lon2):
	# Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = lon1*degrees_to_radians
    theta2 = lon2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    d = arc * 6371 #multiply arc by the radius of the earth 

    return d


data = np.loadtxt('coordinates-mercator.txt')
mappoints = data[:,0:2]
latlons = data[:,2:4]

x = mappoints[:,0]
y = mappoints[:,1]

lats = latlons[:,1]
lons = latlons[:,0]

c1 = fitpoly2d(x,y,lats, order = 2)
c2 = fitpoly2d(x,y,lons, order = 2)

G = nx.read_gpickle(metadatadir + 'network_prefit.gpickle')
pos = nx.get_node_attributes(G,'pos')

fitpos = {k: np.array([float(calcpoly2d(v[0], v[1], c1)), float(calcpoly2d(v[0], v[1], c2))]) for k,v in pos.iteritems()}

nx.set_node_attributes(G,'pos',fitpos)

alpha = 58.8 #Map resolution

L = nx.get_edge_attributes(G,'L')

# v: measured distance in cm
# d: Large-circle distance on earth in km
# p: Length in pixels of straight line between points

fitL = {k: alpha*v*d/p 
		for k,v in L.iteritems()
		for d in [distance(fitpos[k[0]][0], fitpos[k[1]][0], fitpos[k[0]][1], fitpos[k[1]][1])]
		for p in [math.sqrt((pos[k[0]][0]-pos[k[1]][0])**2+(pos[k[0]][1]-pos[k[1]][1])**2)]}


nx.set_edge_attributes(G,'L',fitL)

V = nx.get_edge_attributes(G,'V')

Xbase = {k: (v*1000)**2/100000000 for k,v in V.iteritems()}

X = {k: 0.28*v/vv for k,v in fitL.iteritems() for kk,vv in Xbase.iteritems()}

Y = {k: 1/v for k,v in X.iteritems()}

#pos = nx.get_node_attributes(G,'pos')

#nx.draw(G, pos, node_size=20, with_labels=True)

# G = nx.read_gpickle(metadatadir + 'network_prefit.gpickle')
# pos = nx.get_node_attributes(G,'pos')
# fitpos = {k:func(v,optimal['x'])[::-1] for k,v in pos.iteritems()}
# nx.set_node_attributes(G,'pos',fitpos)

#countrydata = np.loadtxt('bus_countries.csv',dtype = str, delimiter = ',')
#countrydict = {p[0]:p[1] for p in countrydata}

# Xdict = nx.get_edge_attributes(G,'X')
# Ydict = {k:1/v for k,v in Xdict.iteritems()}
# nx.set_edge_attributes(G,'Y',Ydict)


#nx.set_node_attributes(G,'country',countrydict)

nx.write_gpickle(G,metadatadir + 'network_UK_postfit.gpickle')

