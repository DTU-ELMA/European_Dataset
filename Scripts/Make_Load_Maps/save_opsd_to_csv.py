import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pycountry

datadir = '../../Data/OPSD-Load/'
useversion = 'opsd-time_series-2017-07-09'

data = pd.read_csv(os.path.join(datadir, useversion, 'time_series_60min_singleindex.csv'), index_col=0)

loaddata = data[[x for x in data.columns if 'load' in x]]

loadsnip = loaddata.ix[[x for x in loaddata.index if x.startswith('2012-') or x.startswith('2013-') or x.startswith('2014-')]]
loadsnip = loadsnip.dropna('columns')
loadsnip = loadsnip.rename(columns = {c: c.rstrip('_load_old') for c in loadsnip.columns})
loadsnip = loadsnip.rename(columns = {c: pycountry.countries.get(alpha_2=c[:2]).alpha_3 + c[2:] for c in loadsnip.columns})

# Handling missing countries

# Kosovo and Albania are not listed. 2012 consumption from indexmundi.com
c_kosovo = 5.67
c_serbia = 35.5
c_albania = 6.59

loadsnip['ALB'] = loadsnip['SRB']*c_albania/(c_kosovo + c_serbia)
loadsnip['KOS'] = loadsnip['SRB']*c_kosovo/(c_kosovo + c_serbia)

loadsnip.to_csv(os.path.join(datadir, 'opsd_load_data.csv'))
