#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 14:22:18 2022

@author: henry
"""

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-A",
                    dest="A_folder",
                    help="A folder, the code does A - B",
                    default="A_folder")
parser.add_argument("-B",
                    dest="B_folder",
                    help="A folder, the code does A - B",
                    default="B_folder")
args = parser.parse_args()



A_folder = args.A_folder
B_folder = args.B_folder




A_files = os.listdir(A_folder)

B_files = os.listdir(B_folder)


intersect = [itm for itm in A_files if itm in B_files]



for file in intersect:
    os.remove(os.path.join(A_folder,file))
