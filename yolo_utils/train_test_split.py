

import numpy as np
from glob import glob
import os
import argparse
import shutil
from tqdm import tqdm
from imutils import paths
from sklearn.model_selection import train_test_split

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to save train and val dataset",
                    default="data_out")
parser.add_argument("--val-size",
                    type=float,
                    help="size of val size (0.1 default)",
                    default= 0.1)
args = parser.parse_args()



dataset_input = args.dataset_input
#dataset_input = "../../yolo/datasets/dog_dataset/dogs_dataset_yolo/"
dataset_output = args.dataset_output
val_size = args.val_size


def make_train_val_dir(output_dir):
    
    
    for yolo_path in (output_dir,
                      os.path.join(output_dir, 'train', 'labels/'), 
                      os.path.join(output_dir, 'val', 'labels/'),
                      os.path.join(output_dir, 'train', 'images/'), 
                      os.path.join(output_dir, 'val', 'images/')):
        if os.path.exists(yolo_path):
            shutil.rmtree(yolo_path)
        #if not os.path.isdir(dirname):
            #os.mkdir(dirname)

        os.makedirs(yolo_path)    

make_train_val_dir(dataset_output)


my_files = list(paths.list_images(dataset_input))

train_files, val_files = train_test_split(my_files,shuffle=True,test_size=val_size)

# Train files
print("Working on training dataset")
for orig_file_name in tqdm(train_files):
    
    basename = os.path.splitext(os.path.split(orig_file_name)[1])[0]
    orig_txt_file = os.path.join(dataset_input,'labels', basename+".txt")
    
    new_txt_file = os.path.join( dataset_output , 'train', 'labels', basename+".txt")
    new_file_name = os.path.join( dataset_output , 'train', 'images', os.path.basename(orig_file_name))

    shutil.copy(orig_file_name,new_file_name)
    try:
        shutil.copy(orig_txt_file,new_txt_file)
    except Exception as e:
        print(e)
    

# Val files
print("Working on validation dataset")
for orig_file_name in tqdm(val_files):
    
    basename = os.path.splitext(os.path.split(orig_file_name)[1])[0]
    orig_txt_file = os.path.join(dataset_input,'labels', basename+".txt")
    
    new_txt_file = os.path.join( dataset_output , 'val', 'labels', basename+".txt")
    new_file_name = os.path.join( dataset_output , 'val', 'images', os.path.basename(orig_file_name))

    shutil.copy(orig_file_name,new_file_name)
    try:
        shutil.copy(orig_txt_file,new_txt_file)
    except Exception as e:
        print(e)


# Copy classes file
try:
    shutil.copy(os.path.join(dataset_input, 'labels', 'classes.txt'), os.path.join(dataset_output, 'train', 'labels', 'classes.txt'))
except Exception as e:
    print(e)


try:
    shutil.copy(os.path.join(dataset_input, 'labels', 'classes.txt'), os.path.join(dataset_output, 'val', 'labels', 'classes.txt'))
except Exception as e:
    print(e)
