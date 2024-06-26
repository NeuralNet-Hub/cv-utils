"""
This code merge multiple folders and copy them into a single new folder.

Note: All files will be copied

python merge_folders_no_yolo.py -i data_in -o data_out



"""

import os
import argparse
import shutil
from tqdm import tqdm
from imutils import paths


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder to merge",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_out")
args = parser.parse_args()



dataset_input = args.dataset_input
dirname_output_file = args.dataset_output



def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(dirname_output_file)

my_files = list(paths.list_files(dataset_input))

for file0 in tqdm(my_files):
    
    orig_file_name = os.path.join(file0)

    new_file_name = os.path.join(dirname_output_file , os.path.basename(file0))

    shutil.copy(orig_file_name,new_file_name)

        
        
        
        
        
        

        
