"""Create dataset."""
import logging
import os
import subprocess
import sys
import zipfile
from shutil import copy, copyfile, move, rmtree

from py import create_tif
from py import s2a_downloader as s2ad
from py.provide_ground_truth import provide_ground_truth

'''
logging.basicConfig(filename='logfile.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler(stream=sys.stdout)
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setLevel(logging.NOTSET)
logger.addHandler(c_handler)
'''

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(filename='logfile.log', mode='w'),
        logging.StreamHandler()
    ])


logger = logging.getLogger()
logger.handlers[1].setLevel(logging.ERROR)


def make_dataset(date):
    main_dir = '../data/processed_data/' + date
    subdirs = ['/measured_gtiffs', '/prediction_gtiffs', '/ground_truth']

    logger.info('Create directories')

    for subdir in subdirs:
        path = main_dir + subdir
        try:
            os.makedirs(path)
        except OSError:
            if os.path.isdir(main_dir + subdir):
                logger.info("%s already exist." % path)
            else:
                logger.error("Creation of the directory %s failed" % path)
                return

    if os.path.isdir('../data/sentinel_downloads') is False:
        os.makedirs('../data/sentinel_downloads')
    download_exists = s2ad.downloader(date)

    if download_exists is False:
        rmtree(main_dir)
        return

    logger.info('Extract zip-file')

    xml = ''
    if os.path.isdir('../data/sentinel_downloads') == False:
        os.makedirs('../data/sentinel_downloads')
    for fname in os.listdir('../data/sentinel_downloads'):
        if (date in fname) and fname.endswith('.zip'):
            copyfile('../data/sentinel_downloads/' + fname, main_dir + '/' + fname)
            zip_ref = zipfile.ZipFile(main_dir + '/' + fname, 'r')
            extracted = zip_ref.namelist()
            zip_ref.extractall(main_dir)
            xml = extracted[-1]
            zip_ref.close()
            os.remove(main_dir + '/' + fname)

    logger.info('Convert Sentinel Data to GTiff')

    s_start = 'SENTINEL2_L1C:' + main_dir + '/' + xml
    s_names = [s_start+':10m:EPSG_32631', s_start+':20m:EPSG_32631', s_start+':60m:EPSG_32631']

    shell_args = ['./fuse_resolutions.sh'] + s_names +[date]

    subprocess.call(shell_args)

    logger.info('Create GTiffs for measured area')
    create_tif.create_tif(main_dir, 'm')
    logger.info('Create GTiffs for prediction area')
    create_tif.create_tif(main_dir, 'p')

    provide_ground_truth(main_dir, date, xml)
    copy('logfile.log', main_dir + '/logfile.log')
    f = open('logfile.log', 'w')
    f.close()




name = sys.argv[1]

if name.endswith('.txt'):
    datefile = open(name, 'r')
    for line in datefile:
        print(line)
        make_dataset(line[0:8])
else:
    make_dataset(name)

logger.info('DONE')
