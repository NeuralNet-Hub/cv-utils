#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 10:40:36 2022

@author: henry
"""


import pandas as pd
import csv


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    return rgb_color



file_hex = pd.read_csv("hex_color.txt",header=None)
result = list()

java_format = list() #<color name="color"contador>HEXA</color>

for index, color in file_hex.iterrows():
    
    color = color.to_list()[0]
    new_color = hex_to_rgb(color)
    result.append(new_color)
    java_format.append("<color name=\"color"+str(index)+"\">"+str(color)+"</color>")
    



result_df = pd.DataFrame({"c1":result})
result_df.to_csv("rgb_colors.txt", header = None, index = None, sep="\t")


java_df = pd.DataFrame({"c1":java_format})
java_df.to_csv("java_format.txt", header = None, index = None, quoting=csv.QUOTE_NONE)

