#python concatenate_label_files.py -i data_in/labels -o new_labels


import pandas as pd
import os
import argparse
from tqdm import tqdm
import shutil
from imutils import paths


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder that contains labels folder and image folder",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store new concatenated labels data. This directory will be made automatically.",
                    default="labels_new")
parser.add_argument("-l",
                    dest="labels_concat",
                    help="folder with labels you need to concatenate",
                    default="labels_concat")
args = parser.parse_args()






dataset_input = args.dataset_input
dataset_output = args.dataset_output
labels_concat = args.labels_concat

dirname_input_image  = os.path.join( dataset_input  , "images" )
dirname_input_label  = os.path.join( dataset_input  , "labels" )
dirname_output_label = os.path.join(dataset_input, dataset_output)
dirname_concat = labels_concat




def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(dirname_output_label)

# We list images instead of label file, otherwise, some files in the labels_concat won't be loaded
my_images = list(paths.list_images(dirname_input_image))

for image_name0 in tqdm(my_images):
    
    txt_name0 = os.path.join(dirname_input_label,os.path.splitext(os.path.basename(image_name0))[0]+".txt")
    
    if os.path.isfile(txt_name0):
        df_orig = pd.read_csv(txt_name0, sep = " ", header = None)
    else:
        print("Image: " + os.path.basename(image_name0) + " doesn't have txt file")
        df_orig = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5])

    try:
        txt_concat = os.path.join(dirname_concat, os.path.basename(txt_name0))
        df_concat = pd.read_csv(txt_concat, sep = " ", header = None)
        
        df_concat = pd.concat([df_orig, df_concat])
        txt_concat_base = os.path.basename(txt_concat)
        df_concat.to_csv(os.path.join(dirname_output_label, txt_concat_base), sep = " ", header = None, index = None)
        
    except Exception as e:
        print("It wasn't possible to load/concat the file: ")
        print(txt_concat)
        print(e)
        
        

        
shutil.copy(os.path.join(dirname_input_label,"classes.txt"), os.path.join(dirname_output_label, "classes.txt")) 
        
        

        
