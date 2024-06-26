#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 17:01:12 2022

@author: henry

# Usage:
python delete_labels.py -i ~/Projects/synthetic-data-generator/output/ -classes wall floor -copy-orig


"""

import argparse
from tqdm import tqdm
from imutils import paths
import json
import numpy as np
import os
import shutil


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="dataset_input", help="input folder to merge", default="data_in")
parser.add_argument("-o", dest="output_folder", help="output folder", type = str, default="data_out")
parser.add_argument("-classes", nargs='+', dest="classes", help="(string) labels you want to delete, --classes clas0, or --classes clas1 clas2", type = str, default=None)
parser.add_argument("-copy-orig", help="Do you want to copy the original image or just the annotations?", action = 'store_true')

args = parser.parse_args()



dataset_input, classes, output_folder, copy_orig = args.dataset_input, args.classes, args.output_folder, args.copy_orig
classes = [x.lower() for x in classes]

if not os.path.exists(output_folder):
    os.mkdir(os.path.join(output_folder))
        

#dataset_input = "/home/henry/Projects/synthetic-data-generator/output/"
#classes = ["wall", "floor"]

list_images = list(paths.list_images(dataset_input))


total_labels_labelme = 0

for file0 in tqdm(list_images):
    
    image_file_in = file0
    file0 = os.path.splitext(file0)[0]+".json"
    
    
    try:
        
        if os.path.exists(file0):
            with open(file0, 'r') as f:
                data = json.load(f)
        
            index_to_delete = []
            
            for i in range(0, len(data["shapes"])):
                #print(data["shapes"][i]["label"])
                if data["shapes"][i]["label"].lower() in classes:
                    index_to_delete.append(i)    
    
            # Delte unnecesary labels
            shapes = np.delete(np.array(data["shapes"]),index_to_delete)
            data["shapes"] = shapes.tolist()
            
            # Export annotaions
            with open(os.path.join(output_folder,os.path.split(file0)[1]), 'w') as f:
                json.dump(data, f)
            
        if copy_orig:
            image_file_out = os.path.join(output_folder, os.path.split(image_file_in)[1])
            shutil.copy(image_file_in, image_file_out)

    except Exception as e:
        print(e)        
        print("Error in file: " + file0)
        
        
    
    
        

