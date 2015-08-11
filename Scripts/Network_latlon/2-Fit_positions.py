#!/usr/bin/env python

"""2-Fit_positions.py: Fits geographical positions for Bialek grid data."""

__author__ = "Tue Vissing Jensen"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Tue Vissing Jensen"
__email__ = "tvjens@elektro.dtu.dk"

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


metadatadir = '../../Data/Metadata/'

lons = np.load(metadatadir + 'lons.npy')
lats = np.load(metadatadir + 'lats.npy')
onshore = np.load(metadatadir + 'onshore.npy')


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = np.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (np.sin(phi1)*np.sin(phi2)*np.cos(theta1 - theta2) +
           np.cos(phi1)*np.cos(phi2))
    arc = np.arccos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc


def to_fit(pin, pout, coeffs):
    pf = np.array([func(p, coeffs) for p in pin])
    return np.sum((pout-pf)**2)


def func(p, coeffs):
    a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9 = coeffs
    x, y = p
    xs = a0 + a1*x + a2*y + a3*x**2 + a4*y**2 + a5*x*y\
        + a6*x**3 + a7*x**2*y + a8*x*y**2 + a9*y**3
    ys = b0 + b1*x + b2*y + b3*x**2 + b4*y**2 + b5*x*y\
        + b6*x**3 + b7*x**2*y + b8*x*y**2 + b9*y**3
    return np.array([xs, ys])

df = pd.read_csv('coordinates-mercator.txt', delimiter='\t', comment='#')

x = df.x
y = df.y
z = df.lat


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
    X = np.ones(shape=(num_c, len(df.lat)))
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

fitorder = 5

clat = fitpoly2d(x, y, df.lat, fitorder)
clon = fitpoly2d(x, y, df.lon, fitorder)

df['outlat'] = calcpoly2d(x, y, clat)
df['outlon'] = calcpoly2d(x, y, clon)

df.plot(kind='scatter', x='lon', y='lat')
plt.contour(lons, lats, onshore, 1, colors='k')
df.plot(kind='scatter', x='outlon', y='outlat', ax=plt.gca(), c='r')

G = nx.read_gpickle(metadatadir + 'network_prefit.gpickle')
pos = nx.get_node_attributes(G, 'pos')
fitpos = {k: (calcpoly2d(v[0], v[1], clon), calcpoly2d(v[0], v[1], clat)) for k, v in pos.iteritems()}
nx.set_node_attributes(G, 'pos', fitpos)

countrydata = np.loadtxt('bus_countries.csv', dtype=str, delimiter=',')
countrydict = {p[0]: p[1] for p in countrydata}

Xdict = nx.get_edge_attributes(G, 'X')
Ydict = {k: 1/v for k, v in Xdict.iteritems()}
nx.set_edge_attributes(G, 'Y', Ydict)

nx.set_node_attributes(G, 'country', countrydict)

nx.write_gpickle(G, metadatadir + 'network_postfit.gpickle')


raise SystemExit

# # Old method follows

coeffs0 = [df.lat.mean(), 1, 0, 0, 0, 0, 0, 0, 0, 0, df.lon.mean(), 1, 0, 0, 0, 0, 0, 0, 0, 0]
coeffs0 = coeffs0 + np.random.normal(size=len(coeffs0))*0.1

data = np.loadtxt('coordinates-mercator.txt', usecols=(0, 1, 2, 3), skiprows=1)
mappoints = data[:, 0:2]
latlons = data[:, 2:4]

to_opt = lambda z, x=mappoints, y=latlons: to_fit(x, y, z)

optimal = opt.minimize(to_opt, coeffs0, method='Powell', options={'maxfev': 100000, 'maxiter': 50000})
opted = np.array([func(p, optimal['x']) for p in mappoints])

G = nx.read_gpickle(metadatadir + 'network_prefit.gpickle')
pos = nx.get_node_attributes(G, 'pos')
fitpos = {k: func(v, optimal['x'])[::-1] for k, v in pos.iteritems()}
nx.set_node_attributes(G, 'pos', fitpos)
