
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:42:34 2020

@author: rikis
"""


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
import matplotlib.colors as colors

time = 'day'
directory = './'

LAT = np.loadtxt('LAT.txt', delimiter=',')
LON = np.loadtxt('LON.txt', delimiter=',')
mitigation =  np.loadtxt('Parks5LIrrigated.txt', delimiter=',')
reference = np.loadtxt('Reference.txt', delimiter=',')
name = 'Parks5LIrrigated-Reference_T2_'+time


diff = mitigation-reference

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(10,5))
divnorm = colors.TwoSlopeNorm(0, vmin = -1.3, vmax = 0.2)


CS = plt.contourf(LON, LAT, diff, 15,  cmap=plt.cm.hsv_r, norm = divnorm,
             transform=ccrs.PlateCarree())

coastname = './Shapefiles/Costa.shp'
coastlines_10m = cfeature.NaturalEarthFeature('physical', 'coastline', '10m')
coastlines_10m = ShapelyFeature(Reader(coastname).geometries(), ccrs.epsg(25831),
                       linewidth = 1, facecolor = 'None', edgecolor='black')
ax.add_feature(coastlines_10m, facecolor='None', edgecolor='black')
filename = './Shapefiles/AMB31N.shp'
AMB_feature = ShapelyFeature(Reader(filename).geometries(), ccrs.epsg(25831),
                             linewidth = 1, facecolor = 'None', edgecolor='black')
ax.add_feature(AMB_feature)

cbar = fig.colorbar(CS)
cbar.ax.set_ylabel('2m Temperature ($^\circ$C)', size = 12)

plt.savefig(directory+name)