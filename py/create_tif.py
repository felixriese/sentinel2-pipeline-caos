"""Create tif file."""

import logging
import os

import fiona
import rasterio
import rasterio.features
import rasterio.mask
import rasterio.plot
import rasterio.warp

logger = logging.getLogger(__name__)


def create_tif(path, curr_type):
    Type = ''
    if curr_type == 'p':
        Type = 'prediction_area'
    else:
        Type = 'measured_area'

    ind = Type.find('_')
    shpfiles = [file for file in os.listdir('../data/shapefiles/' + Type)
                if file.endswith('.shp')]

    with rasterio.open(path + './data/all_bands.tif') as src:
        profile = src.profile
        for filename in shpfiles:
            shapefile_path = '../data/shapefiles/' + Type + '/' + filename
            with fiona.open(shapefile_path, "r") as shapefile:
                features = [feature["geometry"] for feature in shapefile]
                out_image, out_transform = rasterio.mask.mask(src, features,
                                                              crop=True)
                profile['transform'] = out_transform
                profile['width'] = out_image.shape[2]
                profile['height'] = out_image.shape[1]
                new_filename = (path + '/' + Type[:ind] + '_gtiffs/' +
                                filename[:-4]+'.tif')
                with rasterio.open(new_filename, 'w', **profile) as dst:
                    dst.write(out_image)
