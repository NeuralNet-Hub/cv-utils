

import os
import argparse
import shutil
from tqdm import tqdm
from imutils import paths

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input path of images",
                    default="data_in")
parser.add_argument("-label_folder",
                    dest="new_label_folder",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="label")
args = parser.parse_args()



dataset_input = args.dataset_input
label_folder = args.new_label_folder
dirname_input_image  = os.path.join( dataset_input  , "images" )
dirname_input_label  = os.path.join( dataset_input  , "labels" )


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(label_folder)



my_images = paths.list_images(dirname_input_image)


for image_name0 in tqdm(my_images):
    
    try:
        basename_txt = os.path.splitext(os.path.basename(image_name0))[0]+".txt"
        txt_file_in = os.path.join(dirname_input_label, basename_txt)
        txt_file_out = os.path.join(label_folder, basename_txt)
        shutil.copy(txt_file_in,txt_file_out)
    except Exception as e:
        print(e)
    
    
        
