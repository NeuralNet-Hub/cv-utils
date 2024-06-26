#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:12:32 2022

@author: henry
"""



from imutils import paths
from cv2 import imread
import argparse

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("--source",
                    dest="source",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="train_new")

args = parser.parse_args()

#dataset_input = "data_augmentation_for_yolo/train/"
dataset_input = args.source


list_images=list(paths.list_images(dataset_input))


#corrupted = []

for file in list_images:
    #print(file)
    
    # Read image to get height and width
    imread(file)


#print("These images could be corrupted")
#print(corrupted)