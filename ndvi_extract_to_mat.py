# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 21:18:45 2021

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

#%%
#### get all HDF files in the directory ####
filename=os.listdir(r"E:\MTP2\MODIS NDVI")
nc_files=[]
for file in filename:
    if file.endswith(".hdf"):
        nc_files.append(file)
        
del filename
#%%
xl = np.linspace(-180, 180, 7200)     #x is long
yl = np.linspace(90, -90, 3600)      #y is lat

x_new=sorted(xl[4930:5604])
y_new=sorted(yl[1025:1669])

SM=np.empty((len(nc_files),130,136))
SM[:] = np.NaN

# Default coordinates in file
x=np.array(x_new*644)
y=np.repeat(y_new,674,0)
 # Target coordinates
xj=np.arange(66.5,100.25,0.25).astype('float32')
yj=np.arange(6.5,38.75,0.25).astype('float32')
xi,yi=np.meshgrid(xj,yj)

#%%
for i in range(0,len(nc_files)):
    
    print(i)
    file=str(nc_files[i])
    adress=r"E:\MTP2\MODIS NDVI\\"+file
    
    st=str(file)[9:13]
    #st=st.replace("-","")
    date=int(st)
    
    if (i+1)%12==0:
        date=date*100+12
    else:
        date=date*100+((i+1)%12)
    
    ndv=gdal.Open('HDF4_EOS:EOS_GRID:"'+adress+'":MOD_Grid_monthly_CMG_VI:"CMG 0.05 Deg Monthly NDVI"')
    ndvi_array=ndv.ReadAsArray()
    ndvi_array=ndvi_array/10000
    
    data=(ndvi_array[1025:1669,4930:5604])
    
    z1=np.array(data)
    z1=np.flip(z1,axis=1)
    z1=np.flipud(z1)
    z1=np.reshape(z1,(434056,1))
    zi=griddata((x,y),z1,(xi,yi),method='linear')
    zi=zi[:,:,0]
    
    #setting date, lat and long
    v=np.empty((130,136))
    v[0,0]=date
    v[0,1:136]=xj[:]
    v[1:130,0]=yj[:]
    v[1:130,1:136]=np.fliplr(zi[:,:])

    
    #fixing to 3D array
    SM[i]=v

#%%
check=SM[1,:,:]
#%%
import scipy.io as sio
ndvi_2010_2018={}
ndvi_2010_2018['NDVI']=SM
sio.savemat('ndvi_2010_2018.mat',ndvi_2010_2018)