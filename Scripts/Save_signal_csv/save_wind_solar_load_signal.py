import numpy as np
import pandas as pd
import os

indir = '../../Data/Nodal_Signal/'
outdir = '../../Output_Data/Nodal_TS/'
nodeorder = np.load('../../Data/Metadata/nodeorder.npy')

winddf = pd.concat(
    [pd.DataFrame(
        index=f['dates'],
        data=f['data'],
        columns=map(int, nodeorder)
    ) for filename in sorted(os.listdir(indir)) if 'WND' in filename and 'Siemens' in filename for f in [np.load(indir + filename)]]
)

solardf = pd.concat(
    [pd.DataFrame(
        index=f['dates'],
        data=f['data'],
        columns=map(int, nodeorder)
    ) for filename in sorted(os.listdir(indir)) if 'PVpower' in filename for f in [np.load(indir + filename)]]
)

loaddf = pd.concat(
    [pd.DataFrame(
        index=f['dates'],
        data=f['data'],
        columns=map(int, nodeorder)
    ) for filename in sorted(os.listdir(indir)) if 'load' in filename for f in [np.load(indir + filename)]]
)

winddf = winddf[winddf.index < pd.Timestamp('2015-01-01 00:00:00')]
solardf = solardf[solardf.index < pd.Timestamp('2015-01-01 00:00:00')]
loaddf = loaddf[loaddf.index < pd.Timestamp('2015-01-01 00:00:00')]

winddf.index.name = 'Time'
solardf.index.name = 'Time'
loaddf.index.name = 'Time'

winddf.to_csv(outdir + 'wind_signal.csv', float_format='%.4f')
solardf.to_csv(outdir + 'solar_signal.csv', float_format='%.4f')
loaddf.to_csv(outdir + 'load_signal.csv', float_format='%.4f')

raise SystemExit

# # Interesting plots

# Mean production for each hour of the day, relative to yearly mean.
# Increase of ~50% during midday.
(pd.groupby(df, by=df.index.hour).mean()/df.mean(axis=0)).plot(c='k', alpha=0.1)


w = winddf.mean(axis=1)/winddf.mean().mean()
s = solardf.mean(axis=1)/solardf.mean().mean()
l = loaddf.mean(axis=1)/loaddf.mean().mean()

df = pd.DataFrame(data=np.array([a*w-(1-a)*s-l for a in alphas]).T, columns=alphas, index=w.index)
