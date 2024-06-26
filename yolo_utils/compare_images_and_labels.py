"""
How to run:
python3 rotation.py -i data_in -o data_out -a 15

This code does a match between image and label folders and return those files that don't match 
in these folders

"""

import os
import argparse
from imutils import paths

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_in")

args = parser.parse_args()

#dataset_input = "data_in"
dataset_input = args.dataset_input


list_labels=list(paths.list_files(os.path.join(dataset_input,"labels")))
list_images=list(paths.list_images(os.path.join(dataset_input,"images")))

list_names_images=[]
list_names_labels=[]

for file in list_images:
    file_name=os.path.splitext(os.path.split(file)[1])[0]
    list_names_images.append(file_name)
    
    
for file in list_labels:
    file_name=os.path.splitext(os.path.split(file)[1])[0]
    list_names_labels.append(file_name)

#Remove the file of "classes" from "classes.txt"
try:
    list_names_labels.remove("classes")
except:
    pass

#Match both folders
files_in_labels_not_in_images=[d for d in list_names_labels if d not in list_names_images]

files_in_images_not_in_labels=[d for d in list_names_images if d not in list_names_labels]


print("RESULTS:")
print("=============================================================\n")

#Print results
if len(files_in_labels_not_in_images):
    print("These are the files in labels folder but not in images folder")
    print(files_in_labels_not_in_images)
else:
    print("All files in labels folder are in images folder")
    
    print("\n=============================================================\n")
    
if len(files_in_images_not_in_labels):
    print("These are the files in images folder but not in labels folder")
    print(files_in_images_not_in_labels)
else:
    print("All files in images folder are in labels folder")
    
print("\n=============================================================\n")

