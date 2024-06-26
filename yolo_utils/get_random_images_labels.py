#python get_random_images_labels.py -i train -o data_out -prob


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
parser.add_argument("-prob",
                    dest="prob",
                    help="probability to get the image",
                    type = float,
                    default = 0.5)
args = parser.parse_args()



dataset_input = args.dataset_input
dataset_output = args.dataset_output
prob = args.prob

dirname_input_image  = os.path.join( dataset_input  , "images" )
dirname_input_label  = os.path.join( dataset_input  , "labels" )
dirname_output_image = os.path.join( dataset_output , "images" )
dirname_output_label = os.path.join( dataset_output , "labels" )




def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(dataset_output)
mkdir_p(dirname_output_image)
mkdir_p(dirname_output_label)


my_images = list(paths.list_images(dirname_input_image))

if not os.path.exists(dirname_input_label):
    print("Path: " + dirname_input_label + " doesn't exist , only images will be randomly extracted")


for image_name0 in tqdm(my_images):
    

    if np.random.uniform(0,1) > (1-prob):
        
        
        orig_image_name = os.path.join(image_name0)
        orig_label_name = os.path.join( dirname_input_label , os.path.splitext(os.path.basename(image_name0))[0]+".txt" )
        
        # If txt file exists
        if os.path.exists(orig_label_name):
            
            try:
        
                new_image_name = os.path.join( dirname_output_image , os.path.basename(image_name0))
                new_label_name = os.path.join( dirname_output_label , os.path.splitext(os.path.basename(image_name0))[0]+".txt" )
                
                shutil.copy(orig_label_name,new_label_name)
                shutil.copy(orig_image_name,new_image_name)
                
                
            except Exception as e:
                print(e)
                print("Image not copied")
            
        
        # if not exists file txt then just copy the image
        else: 
            
            try:
        
                new_image_name = os.path.join( dirname_output_image , os.path.basename(image_name0))
                shutil.copy(orig_image_name,new_image_name)
                
                
            except Exception as e:
                print(e)
                print("Image not copied")
        
        
        
try:
    shutil.copy(os.path.join(dirname_input_label,"classes.txt"),os.path.join(dirname_output_label,"classes.txt"))
except Exception as e:
    print(e)
    print("File classes.txt, couldn't be copied")
    
    
    
        

        
