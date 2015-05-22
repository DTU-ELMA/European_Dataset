import numpy as np
import pandas as pd
import os

indir = '/media/tue/Data/Dataset/metadata/'
nodeorder = np.load('/media/tue/Data/Dataset/metadata/nodeorder.npy')

wind_cap = pd.DataFrame(data={'uniform': np.load(indir+'wind_layout_uniform.npy'), 'proportional': np.load(indir+'wind_layout_proportional.npy')}, index=nodeorder)
wind_cap.index.name = 'node'

solar_cap = pd.DataFrame(data={'uniform': np.load(indir+'solar_layout_uniform.npy'), 'proportional': np.load(indir+'solar_layout_proportional.npy')}, index=nodeorder)
solar_cap.index.name = 'node'
wind_cap.to_csv('wind_layouts.csv', float_format='%.4f')
solar_cap.to_csv('solar_layouts.csv', float_format='%.4f')
