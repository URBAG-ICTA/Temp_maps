# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import division
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import datetime
import meteo_functions


my_dpi = 200

##### ALL EDITS HERE ##############################
year1 = 2016 #Initial year as in WRF simulation
year2 = 2016 #Final year as in WRF simulation
month1 = 7 #Initial month as in WRF simulation
month2 = 7 #Final month as in WRF simulation
day1 = 1 #Initial day as in WRF simulation
day2 = 3 #Final day as in WRF simulation
starthour = 12 #Initial hour of the day to do variable average
endhour = 18 #Final hour of the day to do variable average
pathin1 = "C:/Users/1361078/Desktop/Codis_Python/WRFout1/"
pathin2 = "C:/Users/1361078/Desktop/Codis_Python/WRFout2/"
pathout = "C:/Users/1361078/Desktop/Codis_Python/Plots/"
label1 = "BEP-BEM"
label2 = "Bulk"


initial_date = datetime.datetime(year1, month1, day1)
final_date = datetime.datetime(year2, month2, day2)



################ EDITS END HERE ###################

class Temp_map:
    ext         = ''
    num_levels  = 0
    end         = ''
    field       = 0
    LAT         = 0
    LON         = 0 
    colormap    = None
    
    def __init__(self):
        self.num_levels   = 30
        self.ext          = "wrfout_d03_"
        self.end          = '_00.nc'
        self.field        = 0
        self.LAT          = 0
        self.LON          = 0
        self.colormap     = plt.cm.coolwarm
    
    def do_average_Temperature(self, initial_date, final_date, pathin, pathout, starthour, endhour, variable, variable_label, model_label):
        dates = self.simulated_dates(initial_date, final_date)
        self.LAT, self.LON, self.field = self.read_WRFoutputs(variable, dates, pathin, starthour, endhour)
        self.plot_variable(variable, variable_label, model_label)
    
    def plot_variable(self, variable, variable_label, model_label):
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, constrained_layout=True)
        CS = plt.contourf(self.LON, self.LAT, self.field, self.num_levels,  cmap=self.colormap,
             transform=ccrs.PlateCarree())
        coastlines_50m = cfeature.NaturalEarthFeature('physical', 'coastline', '10m')
        ax.add_feature(coastlines_50m, facecolor='None', edgecolor='black')
        cbar = fig.colorbar(CS)
        cbar.ax.set_ylabel(variable_label, size = 12)
        plt.savefig(pathout+variable+"_"+model_label+"_map.png")
        plt.show()

    def simulated_dates(self, initial_day, final_day):
        simulation = final_day - initial_day
        dates = []
        for i in range(0, simulation.days):
            day = initial_day + datetime.timedelta(i)
            dates.append(day.strftime("%Y-%m-%d"))
        return dates
    
    def read_WRFoutputs(self, variable, dates, pathin, starthour, endhour):
        for date in dates:
            file_name = pathin + self.ext + date + self.end
            wfile = Dataset(file_name, 'r')
            if date == dates[0]:
                LON, LAT, LONU, LATU, LONV, LATV = meteo_functions.coordinates(wfile)
                nlat = len(wfile.dimensions['south_north'])
                nlong = len(wfile.dimensions['west_east'])
                my_array = []
                for i in range(nlat):
                    my_array.append([])
                    for j in range(nlong):
                        my_array[i].append([])
            VAR = []
            for data in np.array(wfile.variables[variable]):
                VAR.append(data)
            for hour in range(24):
                if hour >= starthour and hour < endhour:
                    for i in range(nlat):
                        for j in range(nlong):
                            my_array[i][j].append(VAR[hour][i][j])
        my_array = np.array(my_array)
        if variable in ['T2', 'T']:
            my_array -= 273.15
        my_array = np.mean(my_array, axis=2)
        return LAT, LON, my_array
    
def substractTempMaps(temp1, temp2):
    if temp1.LAT.shape == temp2.LAT.shape:
        temp3 = Temp_map()
        temp3.LAT = temp1.LAT
        temp3.LON = temp1.LON
        temp3.field = temp1.field - temp2.field
        return temp3
    else:
        print("Temp_map 1 and Temp_map 2 don't have the same cells")
        return None

        
        
tm = Temp_map()
tm.do_average_Temperature(initial_date, final_date, pathin1, pathout, starthour, endhour, 'T2', 'Temperature ($^\circ$C)', label1) 

tm2 = Temp_map()
tm2.do_average_Temperature(initial_date, final_date, pathin2, pathout, starthour, endhour, 'T2', 'Temperature ($^\circ$C)', label2)

tm3 = substractTempMaps(tm, tm2)
tm3.plot_variable('T2', 'Temperature ($^\circ$C)', 'diff')

            




