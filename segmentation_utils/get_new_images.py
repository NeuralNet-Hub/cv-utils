"""
This code will delete all the images that have json file

Note: All files will be copied

python get_new_images.py -i data_in -o data_out



"""

import os
import argparse
import numpy as np
from tqdm import tqdm
from imutils import paths


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder to merge",
                    default="data_in")
args = parser.parse_args()



dataset_input = args.dataset_input
#dataset_input = "../../height_CTO/Fotos/"

my_files_all = list(paths.list_files(dataset_input))
my_files_json = [pos_json for pos_json in my_files_all if pos_json.endswith('.json')]
my_files_all = np.array(my_files_all)

for file0 in tqdm(my_files_json):
    
    orig_file_name = os.path.join(file0)

    new_file_name = os.path.splitext(file0)
    new_file_name = my_files_all[np.where(np.char.startswith(my_files_all, new_file_name[0]+"."))]
    new_file_name = new_file_name[~np.char.endswith(new_file_name, ".json")]

    os.remove(new_file_name[0])
    os.remove(orig_file_name)
