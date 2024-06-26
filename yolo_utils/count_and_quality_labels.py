"""
The following code count the labels in a folder and check if there are coordinates out of the image

How to run:
python quality_labels.py -i test/
    

"""

import pandas as pd
import os
from imutils import paths
import numpy as np
import cv2
import argparse
from tqdm import tqdm
import time


# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="train_new")

args = parser.parse_args()

#dataset_input = "data_augmentation_for_yolo/train/"
dataset_input = args.dataset_input


list_labels = list(paths.list_files(os.path.join(dataset_input,"labels")))
list_images=list(paths.list_images(os.path.join(dataset_input,"images")))

if os.path.join(dataset_input,"labels/classes.txt") in list_labels:
    names = pd.read_table(os.path.join(dataset_input,"labels/classes.txt"),header=None)
    max_class = len(names)-1
    list_labels.remove(os.path.join(dataset_input,"labels/classes.txt"))
else:
    print("The folder 'labels' doesn't have a 'classes.txt' file")
    1/0

if len(list_images) != len(list_labels):
    print("Images and labels don't have the same length")
    print("LEN LIST IMAGES:")
    print(len(list_images))
    
    print("LEN LIST LABELS:")
    print(len(list_labels))
    time.sleep(10)

list_labels = sorted(list_labels)
list_images = sorted(list_images)

    

names = names.iloc[:,0].to_numpy()

final_df=pd.DataFrame()
l = len(list_labels)
bad_coordinates = []

for i in tqdm(range(0,l)):
    file = list_labels[i]
    #file = 'train/labels/img_34_jpg.rf.3fd8bf12b88180e56245533f8db208fb.txt'
    im_file = list_images[i]
    
    # Read image to get height and width
    my_image=cv2.imread(im_file)
    im_height, im_width, _ = my_image.shape
    
    
    try:
        # Read the label data frame for previous image and concatenate with final_df
        temp_df=pd.read_table(file,header=None,sep=" ")
        final_df=pd.concat([final_df,temp_df])
        
        _, xcenter, ycenter, w, h = temp_df.iloc[0,:]
        
        # Convert to 2D coordinates
        xmin=int((xcenter - w / 2)*im_width)
        ymin=int((ycenter - h / 2)*im_height)
        xmax=int((xcenter + w / 2)*im_width)
        ymax=int((ycenter + h / 2)*im_height)
        
        # Condition for y and x
        cond_y = (0 <= ymin <= im_height) & (0 <= ymax <= im_height)
        cond_x = (0 <= xmin <= im_width) & (0 <= xmax <= im_width)
        
        # If there is a coordinate wrong it's saved in a list
        if not cond_y or not cond_x:
            bad_coordinates.append(file)
        
        
        try:
            if any(temp_df.iloc[:,0] > max_class):
                1/0
        except:
            print("The following file has wrong classes:")
            print(file)
            print("=============================================================")
            print("These area the coordinates for this file:")
            print(temp_df)
            raise
    except:
        print("Following files could have problems, maybe is empty:")
        print(file)
        bad_coordinates.append(file)
    
    

    

# To show the results better:
classes=final_df.iloc[:,0].to_numpy()
count = np.unique(classes,return_counts=True)
count_df = pd.DataFrame(columns=names,index=[0])
count_df.iloc[0,count[0]] = count[1]

print("\n \n RESULTS:\n")
print("=============================================================")
print("TOTAL OF IMAGES:")
print(l)
print("=============================================================")
print("COUNT OF CLASSES:")
print(count_df)
print("=============================================================")

if len(bad_coordinates):
    print("ALERT!! ALERT!! THE FOLLOWING IMAGES COULD HAVE BAD COORDINATES")
    print(bad_coordinates)
else:
    print("ALL COORDINATES HAVE BEEN SUCCESFULLY CHECKED AND THEY APPERENTLY ARE OK!")
    



