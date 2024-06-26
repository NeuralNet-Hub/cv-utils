#python convert_webp_to_jpg.py -i data_in -o data_out 


import numpy as np
import cv2
from glob import glob
import os
import argparse
from tqdm import tqdm

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_rotational")

args = parser.parse_args()


dataset_input = args.dataset_input
dataset_output = args.dataset_output

dirname_input_image  = os.path.join( dataset_input  , "images" )
dirname_output_image = os.path.join( dataset_output , "images" )


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(dataset_output)
mkdir_p(dirname_output_image)


image_names = sorted(glob(dirname_input_image+"/*.webp"))


for image_name0 in tqdm(image_names):
    
    fileoutput = os.path.split(image_name0)[1]
    fileoutput = os.path.splitext(fileoutput)[0]+".jpg"
    fileoutput = os.path.join(dirname_output_image,fileoutput)
    img = cv2.imread(image_name0)
    cv2.imwrite(fileoutput,img)
    