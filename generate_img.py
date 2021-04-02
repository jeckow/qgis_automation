import netCDF4 as nc
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import glob2
from contourf_to_shp import transform


#----------ACCESS ALL CSVS IN DIRECTORY----------
access_csvs = glob2.glob('path to csvs to be analyzed/*.csv')


#----------CREATE NETCDF4 FILE----------
fn = 'path for saving netcdf4/test.nc'
ds = nc.Dataset(fn, 'w', format='NETCDF4')

#create dimensions
time = ds.createDimension('time', None)
lat = ds.createDimension('lat', 37)
long = ds.createDimension('long', 19)S

#create variables
times = ds.createVariable('time', 'f4', ('time',))
lats = ds.createVariable('lat', 'f4', ('lat',))
longs = ds.createVariable('long', 'f4', ('long',))
values = ds.createVariable('value', 'f4', ('time','lat','long',))

# specify units
lats.units = 'DDS'
longs.units = 'DDS'
values.units = 'unkown'


for files in access_csvs:

    #------INTERPOLATE MISSIONG POINTS-------
    file = pd.read_csv(files)
    df = pd.DataFrame(file)
    data = df.to_numpy(dtype = float)

    grid_long, grid_lat = np.mgrid['longitude bounds', 'latitude bounds']
    grid_data = griddata(data[:,1:], np.transpose(np.array([data[:,0]])), (grid_long, grid_lat), method = 'cubic')
    # plt.imshow(grid_data[:,:,0].T, origin = 'lower', cmap='viridis', vmin=0, vmax=40)

    fig = transform(grid_long, grid_lat, grid_data, files[-9:-4])


    # pairs = np.vstack([grid_long.ravel(), grid_lat.ravel()]).T
    # grid_z = grid_data[:,:,0].ravel()

    # mesh_df = pd.DataFrame({'LAT': pairs[:,1], 'LON': pairs[:,0], 'VAL': grid_data[:,:,0].ravel()})
    # mesh_df['coords'] = list(zip(mesh_df['LAT'], mesh_df['LON']))
    # mesh_df['coords'] = mesh_df['coords'].apply(Point)
    # gdf1 = gpd.GeoDataFrame(mesh_df, geometry='coords', crs = {'init': 'epsg 4326'})


    values[access_csvs.index(files),:,:] = grid_data[:,:,0].T
    print(access_csvs.index(files))
    # ds.close()
    # break
ds.close()
