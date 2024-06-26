"""
It will return in a folder random frames according to a parameter

How to run:
python from_video_to_frame.py -i data_in -o data_out -param_chiq 2
    

"""

import cv2
from imutils import paths
import os
import numpy as np
import argparse
from tqdm import tqdm
import pandas as pd


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory where videos are storage, frames will be gotten from all videos of this folder",
                    default="labels")

parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory where frames will be stored",
                    default="labels_output")


args = parser.parse_args()


data_in = args.dataset_input
data_out = args.dataset_output


if not os.path.isdir(data_out):
    os.makedirs(data_out)

list_files=list(paths.list_files(data_in))


for file in tqdm(list_files):
    
    file_name=file.split(os.path.sep)
    file_name=file_name[len(file_name)-1]


    vs = cv2.VideoCapture(file)
    total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    
    labels_df = pd.read_csv(file, header = None, sep = " ")
    
    labels_df = labels_df.replace({0 : { 9 : 0, 11 : 1, 13 : 6}})
    
    labels_df.to_csv(data_out +os.path.sep+ file_name, sep = " ",header= None, index= False)
    
    
