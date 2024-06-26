#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 17:09:40 2022

@author: henry
"""

"""
This code will copy in a new folder the images that contains json

Note: All files will be copied

python get_new_images.py -i data_in -o data_out



"""

import os
import argparse
import numpy as np
from tqdm import tqdm
from imutils import paths
import shutil

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder to merge",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="input folder to merge",
                    default="data_out")
args = parser.parse_args()



dataset_input = args.dataset_input
dataset_input = "Downloads/OneDrive_1_9-5-2022/EPIS (1)/"
dataset_output =  "Projects/synthetic-data-generator/circet/foregrounds/"

my_files_all = list(paths.list_files(dataset_input))
my_files_json = [pos_json for pos_json in my_files_all if pos_json.endswith('.json')]
my_files_all = np.array(my_files_all)

for file0 in tqdm(my_files_json):
    
    orig_file_name = os.path.join(file0)

    image_file_name_orig = os.path.splitext(file0)
    image_file_name_orig = my_files_all[np.where(np.char.startswith(my_files_all, image_file_name_orig[0]+"."))]
    image_file_name_orig = image_file_name_orig[~np.char.endswith(image_file_name_orig, ".json")][0]
    new_image_file_name = os.path.join(dataset_output,os.path.split(image_file_name_orig)[1])

    shutil.copy(image_file_name_orig, new_image_file_name)
