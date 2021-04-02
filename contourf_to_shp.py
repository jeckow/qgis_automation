from shapely import geometry
import numpy as np
import matplotlib.pyplot as plt
import fiona
import os
import geopandas as gpd
import matplotlib as mpl

def transform(grid_long, grid_lat, grid_data, time):

    plt.figure()
    plt.subplot(1,2,1)
    cs = plt.contourf(
        grid_long, grid_lat, grid_data[:,:,0], 30,
        cmap = 'viridis')
    plt.close()
    # plt.colorbar(mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0.0, vmax=40.0), 
                                        # cmap = 'viridis'))


    lvl_lookup = dict(zip(cs.collections, cs.levels))

    # loop over collections (and polygons in each collection), store in list for fiona
    PolyList=[]
    for col in cs.collections:
        z = lvl_lookup[col] # the value of this level

        # convert the countours to shapes
        for contour_path in col.get_paths():

            # create the polygon for this level
            for ncp,cp in enumerate(contour_path.to_polygons()):
                lons = cp[:,0]
                lats = cp[:,1]
                new_shape = geometry.Polygon([(i[0], i[1]) for i in zip(lons, lats)])

                if ncp == 0:
                    poly = new_shape # first shape

                else:
                    poly = poly.difference(new_shape) # Remove the holes

            PolyList.append({'poly':poly,'props':{'z': z}})


    # define ESRI schema, write each polygon to the file
    path = 'path to folder'
    full_path = os.path.join(path, 'path to generated shapefile', f'{time}.shp')
    schema = {'geometry': 'Polygon','properties': {'z': 'float'}}

    # label shapes in shapefile as polygons
    with fiona.collection(full_path, "w", "ESRI Shapefile", schema) as output:
        for p in PolyList:
            output.write({'properties': p['props'],
                'geometry': geometry.mapping(p['poly'])})


    # matching the colormap
    load_contour = gpd.read_file(full_path)
    load_contour.crs = {'init': 'epsg:4326'}

    #ADDING THE TRIMMING LAYER
    trim_layer = gpd.read_file('path to pre-made shapefile for trimming')
    trim_layer.crs = {'init': 'epsg:4326'}

    #GENERATE MAP
    gdf = gpd.read_file('shapefile from basemap')
    gdf = gdf.to_crs(epsg = 4326)

    #COMPUTE DIFFERENCE AND PLOT
    diff = gpd.overlay(load_contour, trim_layer, how = 'difference')
    fig, ax = plt.subplots(figsize = (50, 25))
    ax.set_aspect('equal')
    gdf.plot(ax = ax, color = 'white', edgecolor = 'k')
    print(type(diff))
    diff.plot(ax = ax, column = 'z', cmap = 'magma', vmin = 0, vmax = 40, alpha = 0.8)

    #customize plot accessories/labels
    bar = plt.colorbar(mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0.0, vmax=40.0), cmap = 'magma'), ax = ax, pad = 0.005)
    bar.set_label('color bar title here', rotation = 270, fontsize = 25, labelpad = 40)
    ax.grid(linestyle = '--', alpha = 0.8)
    title = ax.set_title('title here', fontsize = 25)
    plt.text(121.1, 14.37, f'{time[-5:-3]}:{time[-2:]}', fontsize = 25)

    # save each generated image to a folder for gif processing
    fig.savefig(f'file path to save/{time}.png', bbox_inches='tight')

    return diff
