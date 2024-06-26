"""
The following code deletes the classes we don't need it and create a new folder for them

How to run:
python Projects/python_utils/yolo_utils/delete_classes.py -i input -o output

    

"""

import pandas as pd
import os
from imutils import paths
import numpy as np
import argparse
import shutil
from tqdm import tqdm
import cv2

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder which contains 'images' and 'labels' folder data.",
                    default="train_new")
parser.add_argument("-o",
                    dest="output_folder",
                    help="new folder where the labels will be saved",
                    default="data_out")
parser.add_argument("--number",
                    dest="number",
                    help="number from which images will be copied",
                    type=int,
                    default=5)

args = parser.parse_args()

print(args)

dataset_input = args.dataset_input
output_folder = args.output_folder
number  = args.number



if not os.path.exists(output_folder):
    os.mkdir(os.path.join(output_folder))
    
if not os.path.exists(os.path.join(output_folder,"images")):
    os.mkdir(os.path.join(output_folder,"images"))

if not os.path.exists(os.path.join(output_folder,"labels")):
    os.mkdir(os.path.join(output_folder,"labels"))    



list_labels = list(paths.list_files(os.path.join(dataset_input,"labels")))
list_images=list(paths.list_images(os.path.join(dataset_input,"images")))


l = len(list_images)

for i in tqdm(range(0,l)):

    file_image = list_images[i]
    file = os.path.join(dataset_input,"labels",os.path.split(os.path.splitext(list_images[i])[0])[1]+".txt")
    
    try:
    
        # Read the label data frame for previous image and concatenate with final_df
        temp_df=pd.read_csv(file,header=None,sep=" ")
        
        # If the dataset is not empty
        if temp_df.shape[0] >= number:
            
            file_new = os.path.join(output_folder,"labels",os.path.split(file)[1])
            temp_df.to_csv(file_new,sep=" ",header=False,index=False)
            
            img = cv2.imread(file_image)
            h, w, _ = img.shape
            
            if h > 1:
                
                file_image_new = os.path.join(output_folder,"images",os.path.split(file_image)[1])
                
                shutil.copy(file_image,file_image_new)
            
        i+=i+1
    except:
        pass
        #print(temp_df)
        #print("file with labels not found: "+ os.path.split(file)[1])
        
        
