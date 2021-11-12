# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 12:37:13 2021

@author: LIKITH
"""

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import tables
import h5py
import os
import xarray as xr
from scipy.interpolate import griddata 


ndvi=gdal.Open('HDF4_EOS:EOS_GRID:"E:\MTP2\MODIS NDVI\MOD13C2.A2010001.006.2015198205120.hdf":MOD_Grid_monthly_CMG_VI:"CMG 0.05 Deg Monthly NDVI"')
#print(ndvi)
ndvi_array=ndvi.ReadAsArray()
ndvi_array=ndvi_array/10000

xl = np.linspace(-180, 180, 7200)     #x is long
yl = np.linspace(90, -90, 3600)      #y is lat
lon, lat = np.meshgrid(xl, yl)

x_new=sorted(xl[4930:5604])
y_new=sorted(yl[1025:1669])
data=(ndvi_array[1025:1669,4930:5604])

ndvi=np.empty((1,130,136))
ndvi[:] = np.NaN

# Default coordinates in file
x=np.array(x_new*644)
y=np.repeat(y_new,674,0)
 # Target coordinates
xj=np.arange(66.5,100.25,0.25).astype('float32')
yj=np.arange(6.5,38.75,0.25).astype('float32')
xi,yi=np.meshgrid(xj,yj)

#%%
z1=np.array(data)
z1=np.flip(z1,axis=1)
z1=np.flipud(z1)
z1=np.reshape(z1,(434056,1))
zi=griddata((x,y),z1,(xi,yi),method='linear')
zi=zi[:,:,0]

#setting date, lat and long
v=np.empty((130,136))
v[0,0]=2010
v[0,1:136]=xj[:]
v[1:130,0]=yj[:]
v[1:130,1:136]=np.fliplr(zi[:,:])


#%%
#import scipy.io as sio
#ndvi_2010={}
#ndvi_2010['NDVI']=v
#sio.savemat('ndvi.mat',ndvi_2010)
