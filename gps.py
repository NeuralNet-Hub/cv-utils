#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 13:18:14 2022

@author: henry
"""

import serial

#path = '/dev/serial/by-path/pci-0000\:05\:00.3-usb-0\:2\:1.0 '
path = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00'

ser = serial.Serial(path)
#ser = serial.Serial(path, 4800, timeout=1)



def get_gps_coordinates():
    
    try_value = 0
    
    while True:
        
        try:
            line = ser.readline()
            line = line.decode("utf-8")
            
            if "GNGLL" in line:
                
                # Split the line into coordinates
                line = line.split(",")
                lat = line[1] +" " +line[2]
                lon = line[3] + " " + line[4]
                
                # We transform to Google Maps
                lat = float(line[1][0:2]) + (float(line[1][2:len(line[1])])/60)
                lon = -(float(line[3][0:3]) + (float(line[3][3:len(line[3])])/60))
                
                # We have to change sign in case we are not in north or west
                if line[2] != "N":
                    lat = -lat
                if line[4] != "W":
                    lon = -lon
                         


                """
                print("LATITUDE:" + str(lat))
                print("LONGITUDE:" + str(lon))
            

                with open("sample.txt","a+") as f:
                    f.write(str(lat) + " " + str(lon)+"\n")
                """
                return lat, lon
            
        except Exception as e:
            print(e)
            try_value+=1
            print(try_value)
            pass
        
            if try_value >= 10:
                return '', ''
    
    

    

    
# get_gps_coordinates()
