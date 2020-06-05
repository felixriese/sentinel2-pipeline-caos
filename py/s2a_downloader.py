"""Download Sentinel-2a data."""
import configparser
import logging
import os

import numpy as np

import sentinel_api as api  # https://github.com/jonas-eberle/esa_sentinel

logger = logging.getLogger(__name__)
ini = configparser.ConfigParser()
ini.read('account.ini')

def downloader(date):
    for file in os.listdir('../data/sentinel_downloads/'):
        if date in file:
            logger.info('File already exists.')
            return True

    ini = configparser.ConfigParser()
    ini.read('account.ini')
    username = ini['account_data']['username']
    password = ini['account_data']['password']

    if username is '' or password is '':
        logger.error('Account data not specified. Insert username and password in account.ini')
        return False

    s2 = api.SentinelDownloader(username, password, api_url='https://scihub.copernicus.eu/apihub/')
    s2.set_download_dir('../data/sentinel_downloads/')
    s2.load_sites('../data/shapefiles/small_shape/small.shp')

    s2.search('S2A*', filename='*T31UGR_'+date+'*', productType='S2MSI1C', min_overlap=0.9)


    if len(s2.get_scenes()) is 0:
        logger.error('No Sentinel 2 data for the date %s found.' % date)
        return False
    else:
        s2.download_all()
        return True
