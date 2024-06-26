#python convert_webp_to_jpg.py -i data_in -o data_out 


import numpy as np
import cv2
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
                    default="data_out")

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


image_names = os.listdir(dirname_input_image)


for image_name0 in tqdm(image_names):
    
    fileimage = os.path.join(dirname_input_image,image_name0)
    fileoutput = os.path.join(dirname_output_image,image_name0)
    img = cv2.imread(fileimage)
    cv2.imwrite(fileoutput,img)
    