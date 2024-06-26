#python merge_images_labels_folders.py -i train -o data_out


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


dirname_output_image = os.path.join( dataset_output , "images" )
dirname_output_label = os.path.join( dataset_output , "labels" )




def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(dataset_output)
mkdir_p(dirname_output_image)
mkdir_p(dirname_output_label)


my_images = list(paths.list_images(dataset_input))

for image_name0 in tqdm(my_images):
    
    pre_path = image_name0.split(os.sep)[-3]
    
    orig_image_name = os.path.join(image_name0)
    orig_label_name = os.path.join( dataset_input, pre_path, "labels" , os.path.splitext(os.path.basename(image_name0))[0]+".txt" )

    
    new_image_name = os.path.join( dirname_output_image , os.path.splitext(os.path.basename(image_name0))[0]+ "_" +pre_path+".jpg" )
    new_label_name = os.path.join( dirname_output_label , os.path.splitext(os.path.basename(image_name0))[0]+ "_" +pre_path+".txt" )
    
    
#    if os.path.exists(new_image_name):
#        break
    
    shutil.copy(orig_image_name,new_image_name)
    try:
        shutil.copy(orig_label_name,new_label_name)
    except Exception as e:
        print(e)
        
        
        
        
        
        

        
