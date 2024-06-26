#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:15:11 2021

@author: henry
"""

import os
import cv2
from glob import glob

output_folder = "data_out"

list_images = glob("google_moto/images/"+"/*")

for filename in list_images:
    
    fileoutput = os.path.split(filename)[1]
    image_ext = os.path.splitext(fileoutput)[1]
    fileoutput = os.path.splitext(fileoutput)[0]
    fileoutput = os.path.join(output_folder,fileoutput)+"_flip"+image_ext
    
    img = cv2.imread(filename)
    img = img[:, ::-1, :]
    cv2.imwrite(fileoutput, img)