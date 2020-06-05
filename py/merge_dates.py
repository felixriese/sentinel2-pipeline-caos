"""Merge dates."""
import os

import numpy as np
import pandas as pd
import rasterio

locs = ['M_C', 'M_D', 'M_E', 'M_F', 'M_G', 'M_H', 'S_I', 'S_J', 'S_K', 'S_L',
        'S_P', 'S_Q', 'S_R', 'Sa_J', 'Sa_K', 'Sa_L']
cols = ['Date', 'Station', 'VWC_Avg.3.', 'VWC_Avg.6.', 'VWC_Avg.9.',
        'EC_Avg.3.', 'EC_Avg.6.', 'EC_Avg.9.', 'Temp5TE_C_Avg.3.',
        'Temp5TE_C_Avg.6.', 'Temp5TE_C_Avg.9.', 'AirTemp_C_Avg', 'RelHumid',
        'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'b11',
        'b12', 'b8a']


df_tot = pd.DataFrame(columns=cols)

for curr_dir in os.listdir('./processed_data/'):
    if curr_dir.startswith('201'):
        print(curr_dir)
        for loc in locs:
            print(loc)
            try:
                df_csv = pd.read_csv(
                    '../data/processed_data/'+curr_dir+'/ground_truth/'+loc+'.csv')
                if df_csv.empty:
                    break
            except FileNotFoundError:
                break
            cols_csv = df_csv.columns.values.tolist()
            params = []
            for parameter in cols_csv[1:]:
                mean = np.mean(np.sort(df_csv[parameter])[3:-3])
                params.append(mean)

            bands = []
            with rasterio.open('../data/processed_data/'+curr_dir+'/measured_gtiffs/'+loc+'.tif') as src:
                for idx in src.indexes:
                    mean = np.mean(np.sort(src.read(idx)).flatten()[1:-1])
                    bands.append(mean)
            keys = cols
            values = [curr_dir, loc]
            values.extend(params)
            values.extend(bands)
            row = dict(zip(keys, values))
            df_tot = df_tot.append(row, ignore_index=True)


VWC_Avg = []
for i in df_tot.index.tolist():
    x = np.array([df_tot['VWC_Avg.3.'][i],df_tot['VWC_Avg.9.'][i]])
    VWC_Avg.append(np.nanmean(x))

df_tot = df_tot.drop(columns=['VWC_Avg.3.', 'VWC_Avg.6.', 'VWC_Avg.9.'])

df_tot['VWC_Avg.'] = pd.Series(VWC_Avg, index=df_tot.index)

df_tot.to_csv('../data/processed_data/merged_dataset.csv', sep=';', na_rep='NA')
