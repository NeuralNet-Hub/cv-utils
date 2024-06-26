#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 17:29:06 2022

@author: henry
"""


from imutils import paths
import cv2
import os
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_out")
parser.add_argument('-counter',
                    action='store_true',
                    help='COUNTERCLOCKWISE rotation')

args = parser.parse_args()


dataset_input = args.dataset_input
dataset_output = args.dataset_output


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(dataset_output)


list_images = list(paths.list_images(dataset_input))


for image in list_images:  
    # Reading an image in default mode
    im0 = cv2.imread(image)
      

    if args.counter:
        im0_rot = cv2.rotate(im0, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        im0_rot = cv2.rotate(im0, cv2.ROTATE_90_CLOCKWISE)
    
    
    cv2.imwrite(os.path.join(dataset_output,os.path.split(image)[1]),im0_rot)