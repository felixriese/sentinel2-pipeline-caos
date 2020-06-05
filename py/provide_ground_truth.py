"""Provide ground truth."""

import logging
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)

def provide_ground_truth(main_dir, date, xml):
    ind = xml.find('T')
    time = xml[ind+1:ind+7]
    overpass_time = datetime.strptime(date+time, '%Y%m%d%H%M%S')
    lower_time = overpass_time - timedelta(minutes=30)
    upper_time = overpass_time + timedelta(minutes=30)

    if sorted(os.listdir('../data/ground_truth')) == sorted(os.listdir(
            main_dir + '/ground_truth/')):
        logger.info("CSV files already exist.")
        return

    for file in tqdm(os.listdir('../data/ground_truth'), desc='Create csv for %s .' % date):
        logger.info('Extract data from %s' % file)
        df = pd.read_csv('../data/ground_truth/' + file, sep=',',index_col=0)
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
        new_df = df[((df['TIMESTAMP']>lower_time)&(df['TIMESTAMP']<upper_time))]
        if new_df.empty:
            cols = df.columns.values.tolist()
            a = numpy.empty(len(cols))
            a[:] = numpy.nan
            d = dict(zip(cols, a))
            new_df = pd.DataFrame(data=d)
        new_df.to_csv(main_dir + '/ground_truth/'+file, sep=',', na_rep='NA', index=False)
