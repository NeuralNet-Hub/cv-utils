#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:53:19 2022

@author: henry
"""


import shutil
import os
import argparse






parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest = "input_path",
                    help = "input folder which contains all the videos",
                    default = "data_in")
parser.add_argument("-o",
                    dest = "output",
                    help = "name of outputfile, by default merged.mp4",
                    default = "epis_val")


args = parser.parse_args()


# Get all arguments
input_path = args.input_path
input_path = "../../Downloads/validation/"
output = args.output

def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(output)



# List files in folders and subfolders

list_files = []
extensions = [".mp4"]

for path, subdirs, files in os.walk(input_path):
    for name in files:
        list_files.append(os.path.join(path, name))



for video in list_files:
    print(video)
    
    shutil.copy(video, os.path.join(output,os.path.split(video)[1]))
        
        
        
        
        
