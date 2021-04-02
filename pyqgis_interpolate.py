from PyQt5.QtWidgets import QApplication
from qgis.core import QgsProcessing
from qgis.core import *
import pandas as pd
import numpy as np

# set file paths
map_path = 'path to map shapefile'
file_path = 'path to csv data'
dataset = f'file:///{file_path}?encoding=%s&delimiter=%s&xField=%s&yField=%s&crs=%s' % ("UTF-8",",", "LON", "LAT", "epsg:4326")

# setup QGIS project
registry = QgsProject.instance()

# declare layers
basemap = QgsVectorLayer(map_path, 'basemap')
# stations = QgsVectorLayer(stations_path, 'stations')
stations_data = QgsVectorLayer(dataset, 'select column', 'delimitedtext')

# plot layers
plot_map = registry.addMapLayer(basemap)

# plot_stations = registry.addMapLayer(stations)
plot_data = registry.addMapLayer(stations_data)

# load layer styles
basemap.loadNamedStyle('path to map_style.qml')
basemap.triggerRepaint()

plot_data.loadNamedStyle('path to stations_style.qml')
plot_data.triggerRepaint()

# read csv data
df = pd.read_csv(file_path, encoding = 'latin-1')

# create array for column indices
csv_columns = range(4,len(df.columns))

for column in csv_columns:
    # IDW interpolation
    idw_params = {
                'DISTANCE_COEFFICIENT': 2,
                'EXTENT': '120.879903585,121.165952446,14.323853961,14.804996053 [EPSG:4326]',
                'INTERPOLATION_DATA': f'file:///{file_path}?encoding=UTF-8&delimiter=,&xField=LON&yField=LAT&crs=epsg:4326::~::0::~::{column}::~::0',
                'PIXEL_SIZE': 0.01,
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }

    idw_result = processing.run('qgis:idwinterpolation', idw_params)
    raster_layer = QgsRasterLayer(idw_result['OUTPUT'], f'interpolated_{column}')
    # plot_raster = registry.addMapLayer(raster_layer)

    # convert raster pixels to point values
    values_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': idw_result['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }

    values_result = processing.run('native:pixelstopoints', values_params)
    #values_layer = QgsVectorLayer(values_result['OUTPUT'], 'temp_values')


    # add X/Y fields to layer
    csv_name = df.columns[column].replace(':','-')

    if column < 12:
        csv_name = f'0{csv_name}'

    coordinates_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'INPUT': values_result['OUTPUT'],
            'PREFIX': '',
            'OUTPUT': f'/path to csv file/{csv_name}.csv'
    }

    coordinates_result = processing.run('native:addxyfields', coordinates_params)
    coordinates_layer = QgsVectorLayer(coordinates_result['OUTPUT'], 'data_points', 'delimitedtext')
