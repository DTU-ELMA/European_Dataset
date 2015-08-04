import numpy as np
import xlrd
import os
import pandas as pd

indir = '../../Data/ENTSOE-load/excel_files/'
outdir = '../../Data/ENTSOE-load/extracted_load/'

# Kosovo and Albania are not listed. 2012 consumption from indexmundi.com
c_kosovo = 5.67
c_serbia = 35.5
c_albania = 6.59

filestoload = [f for f in os.listdir(indir)]

for filename in filestoload:
    print filename

    df = pd.read_excel(indir + filename,sheetname='hourly_load_values', skiprows=6,parse_cols='C:AA')
    data = df.values.flatten()
    data[data == 0] = np.nan
    data[data == ' '] = np.nan
    data=data.astype(float)
    data=data[~np.isnan(data)]
    if 'SRB' in filename:
        kosovo_data = data*c_kosovo/(c_kosovo + c_serbia)
        np.save(outdir + 'KOS_'+filename.split('_')[1].rsplit('.')[0]+'.npy', kosovo_data)
        albania_data = data*c_albania/(c_kosovo + c_serbia)
        np.save(outdir + 'ALB_'+filename.split('_')[1].rsplit('.')[0]+'.npy', albania_data)
        data *= c_serbia/(c_kosovo + c_serbia)
    np.save(outdir + filename.rsplit('.')[0]+'.npy', data)
