import numpy as np
import pandas as pd
import os

indir = '../../Data/Nodal_Forecasts/'
outdir = '../../Output_Data/Nodal_FC/'
nodeorder = np.load('../../Data/Metadata/nodeorder.npy')


for fcdir in sorted(os.listdir(indir)):
    print fcdir
    for filename in os.listdir(indir+fcdir):
        if 'WND' in filename and 'Siemens' in filename:
            f = np.load(indir + fcdir + '/' + filename)
            winddf = pd.DataFrame(
                index=f['dates'],
                data=f['data'],
                columns=map(int, nodeorder)
            )
        if 'PVpower' in filename:
            f = np.load(indir + fcdir + '/' + filename)
            solardf = pd.DataFrame(
                index=f['dates'],
                data=f['data'],
                columns=map(int, nodeorder)
            )

    winddf.index.name = 'Time'
    solardf.index.name = 'Time'
    try:
        winddf.to_csv(outdir + fcdir + '/wind_forecast.csv', float_format='%.4f')
        solardf.to_csv(outdir + fcdir + '/solar_forecast.csv', float_format='%.4f')
    except IOError:
        os.mkdir(outdir + fcdir)
        winddf.to_csv(outdir + fcdir + '/wind_forecast.csv', float_format='%.4f')
        solardf.to_csv(outdir + fcdir + '/solar_forecast.csv', float_format='%.4f')
