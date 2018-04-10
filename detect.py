#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import subprocess
import os
from subprocess import call
import csv

#change offset here
offset_peak = 45.0
offset_rsm = 40.0
header_csv = ("time", "amplitude", "rms")

try:
    while True:
        #pkill because sometimes my microphone was busy
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        time.sleep( 1 )
        
        #time
        filedate = time.strftime("%Y%m%d-%H%M%S")
        filename = "/home/pi/noise/mp3/" + time.strftime("%Y%m%d") + "/" + filedate + ".mp3"
        filename_csv = "/home/pi/noise/csv/" + time.strftime("%Y%m%d") + ".csv"
        filedate_csv  = time.strftime("%Y-%m-%d %H:%M")
        terminal_time = time.strftime("%H:%M ")
        
        #record
        subprocess.call("arecord -D hw:1,0 -d 120 -v --fatal-errors --buffer-size=192000 -f dat -t raw --quiet | lame -r --quiet --preset standard - " + filename,shell= True)
        proc = subprocess.getoutput("sox " + filename + " -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2")
        proc_rms = subprocess.getoutput("sox " + filename + " -n stat 2>&1 | grep 'RMS.*amplitude' | cut -d ':' -f 2")
        os.system('clear')
        proc1 = proc.strip()
        proc1 = float(proc1)
        proc_rms = proc_rms.strip()
        proc_rms = float(proc_rms)
        
        #test your microphone in 5 dB steps and create the function e.g. with mycurvefit.com
        #Fkt 3 30-80 dB
        proc3 = 83.83064 + (28.34183 - 83.83064)/(1 + (proc1/0.04589368)**1.006258)
        #Fkt RMS 30-80 dB
        proc3_rms = 87.69054 + (23.81973 - 87.69054)/(1 + (proc_rms/0.01197014)**0.7397556)
        
        #add db filextentions: peak - rms
        ext_peak = int(round(proc3, 0))
        ext_rms = int(round(proc3_rms, 0))
        
        
        print("Measured values: " + str(proc1) + " / " + str(proc_rms) + " / " + str(proc3) + " / " + str(proc3_rms) + " / " + str(ext_peak) + "\n")
        
        #csv
        file_exists = os.path.isfile(filename_csv)
        daten_csv = (filedate_csv, proc3, proc3_rms)
        with open(filename_csv, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header_csv)
            writer.writerow(daten_csv)
        
        if proc3 >= offset_peak or proc3_rms >= offset_rsm:
                    print(terminal_time + "Sound detected - save: " + filedate + ".mp3 \n")
                    os.rename(filename, "/home/pi/noise/mp3/" + time.strftime("%Y%m%d") + "/" + filedate + "-" + str(ext_peak) + "-" + str(ext_rms) + ".mp3")
                    time.sleep( 3 )
                    #os.system('clear')
                    
        else: 
            print(terminal_time + "No sound detected, delete: " + filedate + ".mp3 \n")
            os.remove(filename)
            time.sleep( 3 )
            #os.system('clear')
            
except KeyboardInterrupt:
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        print('End')