#python get_random_images_labels.py -i train -o data_out


import numpy as np
from glob import glob
import os
import argparse
import shutil
from tqdm import tqdm
from imutils import paths


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_out")
args = parser.parse_args()



dataset_input = args.dataset_input
dataset_output = args.dataset_output


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(dataset_output)

my_files = list(paths.list_files(dataset_input))

for orig_file_name in tqdm(my_files):
    
    previous_folder = os.path.split(os.path.split(orig_file_name)[0])[1]
    
    new_file_name = os.path.join( dataset_output , previous_folder +'_' + os.path.basename(orig_file_name))

    shutil.copy(orig_file_name,new_file_name)
        
        
        
        
        
        

        
