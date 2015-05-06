import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import ndimage

f = ndimage.imread('onshore.png')
# raise SystemExit

onshore = np.sum(f, axis=2) > 400

#raise SystemExit

lats = np.arange(21, 73+0.001, 0.01)
# Offset due to definition of grid
lons = np.arange(-44, 66+0.001, 0.01)+0.05
long, latg = np.meshgrid(lons, lats)


# reverse lat order due to image loading convention.
np.savez('../onshore-interpolator.npz', lons=long, lats=latg[::-1], onshore=onshore)
