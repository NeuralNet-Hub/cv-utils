#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 17:01:12 2022

@author: henry
"""

import argparse
from tqdm import tqdm
from imutils import paths
import json


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder to merge",
                    default="data_in")
args = parser.parse_args()



dataset_input = args.dataset_input
dataset_input = "../../height_CTO/00_datasetV1/images/"

my_files_all = list(paths.list_files(dataset_input))
my_files_json = [pos_json for pos_json in my_files_all if pos_json.endswith('.json')]


total_labels_labelme = 0

for file0 in tqdm(my_files_json):
    
    with open(file0, 'r') as f:
        data = json.load(f)

    total_labels_labelme += len(data["shapes"])



print("\n============================================")
print("YOU HAVE "+str(len(my_files_json)) + " FILES")
print("AND "+ str(total_labels_labelme) + " LABELS")
print("============================================")