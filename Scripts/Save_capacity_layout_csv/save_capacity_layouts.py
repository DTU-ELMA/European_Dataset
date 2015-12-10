import numpy as np
import pandas as pd
import os

indir = '../../Data/Metadata/'
outdir = '../../Output_Data/Metadata/'
nodeorder = np.load('../../Data/Metadata/nodeorder.npy')

wind_cap = pd.DataFrame(data={'Uniform': np.load(indir+'wind_layout_uniform.npy'), 'Proportional': np.load(indir+'wind_layout_proportional.npy')}, index=nodeorder)
wind_cap.index.name = 'node'

solar_cap = pd.DataFrame(data={'Uniform': np.load(indir+'solar_layout_uniform.npy'), 'Proportional': np.load(indir+'solar_layout_proportional.npy')}, index=nodeorder)
solar_cap.index.name = 'node'
wind_cap.to_csv(outdir + 'wind_layouts_ECMWF.csv', float_format='%.4f')
solar_cap.to_csv(outdir + 'solar_layouts_ECMWF.csv', float_format='%.4f')

wind_cap_cosmo = pd.DataFrame(data={'Uniform': np.load(indir+'wind_layout_uniform_COSMO.npy'), 'Proportional': np.load(indir+'wind_layout_proportional_COSMO.npy')}, index=nodeorder)
wind_cap_cosmo.index.name = 'node'

solar_cap_cosmo = pd.DataFrame(data={'Uniform': np.load(indir+'solar_layout_uniform_COSMO.npy'), 'Proportional': np.load(indir+'solar_layout_proportional_COSMO.npy')}, index=nodeorder)
solar_cap_cosmo.index.name = 'node'
wind_cap_cosmo.to_csv(outdir + 'wind_layouts_COSMO.csv', float_format='%.4f')
solar_cap_cosmo.to_csv(outdir + 'solar_layouts_COSMO.csv', float_format='%.4f')
