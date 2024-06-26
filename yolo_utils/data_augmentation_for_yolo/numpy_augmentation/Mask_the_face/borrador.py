#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:00:09 2021

@author: henry
"""


import os
import pandas as pd
import shutil

list_labels = os.listdir("train/labels/")
total = len(list_labels)

for i in range(0,total):
    print(str(i)+" from "+str(total))
    
    file="train/labels/"+list_labels[i]
    dst = file.split("/")
    dst = "/".join(dst[1:len(dst)])
    dst = "out/"+dst
    splitted = file.split("_")
    orig = "_".join(splitted[0:(len(splitted)-1)]) + ".txt"
    
    try:
        shutil.copy2(orig,dst)
        #'nm0683467_rm75733760_1985-11-27_2003_surgical_green.txt'
    except:
        print("File:")
        print(orig)
    
    