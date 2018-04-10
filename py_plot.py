#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from matplotlib import rcParams
from datetime import timedelta, date
import matplotlib.patches as mpatches
from matplotlib.ticker import AutoMinorLocator


tomorrow = date.today() - timedelta(days=1)

filename_csv = "/home/pi/noise/csv/" + tomorrow.strftime("%Y%m%d") + ".csv"
i = int(tomorrow.strftime("%Y"))
j = int(tomorrow.strftime("%m"))
k = int(tomorrow.strftime("%d"))
title_date = tomorrow.strftime('%d.%m.%Y')
pic_title = tomorrow.strftime('%Y-%m-%d')

#csv
with open(filename_csv) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    
    dates, highs, rms = [], [], []
    for row in reader:
        
        current_date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M")
        dates.append(current_date)

        high = float(row[1])
        highs.append(high)

        rms1 =  float(row[2])
        rms.append(rms1)

#locators for x axis
rcParams['axes.titlepad'] = 15

fig, ax = plt.subplots()
hours = mdates.HourLocator(interval = 2)
h_fmt = mdates.DateFormatter('%H:%M')

#Patches
peak_patch = mpatches.Patch(color='red', label='Maximum Amplitude')
rms_patch = mpatches.Patch(color='navy', label='Mean')
plt.legend(handles=[peak_patch, rms_patch])

#For a scatter plot use this: ax.scatter(dates, highs, color = 'red', linewidth = 0.1, s=4)
ax.plot(dates, highs, color = 'red', linewidth = 0.5)
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(h_fmt)

ax.plot(dates, rms, color = 'navy', linewidth = 0.5)

#minorlocator for quarter of an hour 
minor_locator = AutoMinorLocator(8)
ax.xaxis.set_minor_locator(minor_locator)
plt.grid(which='minor', linestyle=':')

#Title,Label
plt.ylabel('noise level in dB', fontsize=12)
plt.title('Noise Level Protocol of ' + title_date, fontsize=15)
plt.grid(True)

#y axis
plt.ylim (    
    ymin = 20,
    ymax = 80    
)

#noise limit
plt.axhline(y=40, color = 'firebrick', linewidth = 0.8)

#x axis
plt.xlim(
    
    xmin = datetime.datetime(i,j,k,0,0,0),
    xmax = datetime.datetime(i,j,k,23,59,0)
)
fig.autofmt_xdate()
fig.set_size_inches(14,10)
plt.savefig('/home/pi/noise/pic/' + pic_title + '.png', bbox_inches='tight')