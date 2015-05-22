import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import ndimage

f = ndimage.imread('countries6.png', flatten = True)

lats = np.arange(73 - 6614*0.011625, 73.000000, 0.011625)
# Offset due to definition of grid
lons = np.arange(-42.743929, -42.743929 + 9354*0.011625, 0.011625)
olons, olats = np.meshgrid(lons, lats)


countries = f


# reverse lat order due to image loading convention.
np.savez('../countries-interpolator.npz', lons=olons, lats=olats[::-1], countries=countries)
