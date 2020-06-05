#!/bin/bash


gdalwarp -q -overwrite -of GTiff -cutline ../shapefiles/small_shape/small.shp -crop_to_cutline $1 processed_data/${4}/10m.tif
gdalwarp -q -overwrite -of GTiff -cutline ../shapefiles/small_shape/small.shp -crop_to_cutline $2 processed_data/${4}/20m.tif
gdalwarp -q -overwrite -of GTiff -cutline ../shapefiles/small_shape/small.shp -crop_to_cutline $3 processed_data/${4}/60m.tif


gdalbuildvrt -q -tr 10 10 -b 1 ${4}_bands_4.vrt ../processed_data/${4}/10m.tif
gdalbuildvrt -q -tr 10 10 -b 2 ${4}_bands_3.vrt ../processed_data/${4}/10m.tif
gdalbuildvrt -q -tr 10 10 -b 3 ${4}_bands_2.vrt ../processed_data/${4}/10m.tif
gdalbuildvrt -q -tr 10 10 -b 4 ${4}_bands_8.vrt ../processed_data/${4}/10m.tif

gdalbuildvrt -q -tr 10 10 -b 1 ${4}_bands_5.vrt ../processed_data/${4}/20m.tif
gdalbuildvrt -q -tr 10 10 -b 2 ${4}_bands_6.vrt ../processed_data/${4}/20m.tif
gdalbuildvrt -q -tr 10 10 -b 3 ${4}_bands_7.vrt ../processed_data/${4}/20m.tif
gdalbuildvrt -q -tr 10 10 -b 4 ${4}_bands_8a.vrt ../processed_data/${4}/20m.tif
gdalbuildvrt -q -tr 10 10 -b 5 ${4}_bands_11.vrt ../processed_data/${4}/20m.tif
gdalbuildvrt -q -tr 10 10 -b 6 ${4}_bands_12.vrt ../processed_data/${4}/20m.tif

gdalbuildvrt -q -tr 10 10 -b 1 ${4}_bands_1.vrt ../processed_data/${4}/60m.tif
gdalbuildvrt -q -tr 10 10 -b 2 ${4}_bands_9.vrt ../processed_data/${4}/60m.tif
gdalbuildvrt -q -tr 10 10 -b 3 ${4}_bands_10.vrt ../processed_data/${4}/60m.tif

# order bands according to EuroSAT

gdal_merge.py -q -separate -of GTiff  -o ../processed_data/${4}/all_bands.tif ${4}_bands_1.vrt ${4}_bands_2.vrt ${4}_bands_3.vrt ${4}_bands_4.vrt ${4}_bands_5.vrt ${4}_bands_6.vrt ${4}_bands_7.vrt ${4}_bands_8.vrt ${4}_bands_9.vrt ${4}_bands_10.vrt ${4}_bands_11.vrt ${4}_bands_12.vrt ${4}_bands_8a.vrt

rm ${4}_bands_*.vrt
