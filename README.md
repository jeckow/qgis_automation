# qgis_automation
Automate generating IDW interpolation data using pyqgis/python. Interpolated data are transforme into points where it can be further processed natively in python

folder properties:
1. qml folder
- This is where you the qml files used to style the shape/raster/csv files
- Used as an input to .loadNamedStyle('file path')

2. pyqgis_interpolate variable properties
- map_path = file path of the shapefile for generating the basemap
- file_path = file path for the csv files to be analyzed'
- dataset = parses the file_path into its proper format

information about the qgis functions used can be found in the qgis documentation:
https://qgis.org/pyqgis/3.0/index.html
