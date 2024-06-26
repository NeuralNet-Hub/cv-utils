#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:53:19 2022

@author: henry
"""


import cv2
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
                    default = "merged.mp4")
parser.add_argument("-fps",
                    dest = "fps",
                    help = "fps rate of the output",
                    type = int,
                    default=30)

args = parser.parse_args()


# Get all arguments
input_path = args.input_path
output = args.output
fps = args.fps


# List files in folders and subfolders

list_files = []
extensions = [".mp4"]

for path, subdirs, files in os.walk(input_path):
    for name in files:
        if os.path.splitext(name)[1] in extensions:
            list_files.append(os.path.join(path, name))


# Get features from the first video only
vcap = cv2.VideoCapture(list_files[0])

fps = int(vcap.get(cv2.CAP_PROP_FPS))
_, frame = vcap.read() 
h, w, _ = frame.shape

# Initialize video writer
vid_writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))



for video in list_files:
    print(video)
    
    
    vcap = cv2.VideoCapture(video)
    total_frames = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))    
        
    while True:
        
        grabbed, im0 = vcap.read()
        
        if not grabbed:
            break
        
        #print(grabbed)        
        #print(im0.shape)
        
        cv2.imshow("0", im0)
        cv2.waitKey(1)  # 1 millisecond
        
        vid_writer.write(im0)
        
        
        
        
        
