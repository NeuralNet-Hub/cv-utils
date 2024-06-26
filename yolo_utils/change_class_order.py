

import pandas as pd
import numpy as np
import os
import argparse
from tqdm import tqdm
from imutils import paths
import shutil


data = {'old': [-1, 1], 'new': [0, 1]}
data = {'old': [0,1,2], 'new': [0,0,0]}

names_new = pd.DataFrame(data)




parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder which contains 'images' and 'labels' folder data.",
                    default="../../yolo/datasets/boxes_counting/mentos_bunched12.v2i.yolov8/test/")
parser.add_argument("-o",
                    dest="output_folder",
                    help="new folder where the labels will be saved")
parser.add_argument("-classes_file",
                    dest="classes_file",
                    help="if you have a defined classes file, the code will match the names and \'data\' dictionary won't be considered")

args = parser.parse_args()
print(args)

dataset_input = "train"
output_folder ="train_new"
dataset_input = args.dataset_input
output_folder = args.output_folder if args.output_folder is not None else dataset_input
classes_file = args.classes_file

if not os.path.exists(output_folder):
    os.mkdir(os.path.join(output_folder))

if not os.path.exists(os.path.join(output_folder,"labels_new")):
    os.mkdir(os.path.join(output_folder,"labels_new"))    

if classes_file is not None:
    # Read new and old classes file
    new_classes = pd.read_table(classes_file,header=None, sep=" ")
    new_classes["idx"] = range(0,new_classes.shape[0])
    old_classes = pd.read_table(os.path.join(dataset_input,"labels","classes.txt"),header=None, sep=" ")
    old_classes["idx"] = range(0,old_classes.shape[0])
    
    # Comparing both data frames and get idexes
    merge_idx = old_classes.merge(new_classes, left_on=0, right_on=0,suffixes=("old","new"))
    data = {'old': list(range(0,old_classes.shape[0])), 'new': ['']*old_classes.shape[0]} # columns '' as empty
    indexes = merge_idx["idxold"].to_list()
    replacements = merge_idx["idxnew"].to_list()
    
    # Replace according to indexes
    for i, index in enumerate(indexes):
        data["new"][indexes[i]] = replacements[i]
    names_new = pd.DataFrame(data)
    
    
    

list_labels = list(paths.list_files(os.path.join(dataset_input,"labels")))



l = len(list_labels)

for i in tqdm(range(0,l)):
    
    file = list_labels[i]

    try:
        file_new = os.path.join(output_folder,"labels_new",os.path.split(file)[1])
        
        # read file line by line into a list
        with open(file, 'r') as my_file_labels:
            content = my_file_labels.readlines()
        
        # create an empty pandas data frame
        my_df = pd.DataFrame()
        
        # iterate over each line in the file
        for line in content:
            # split the line by whitespace
            columns = line.strip().split()
        
            # create a pandas data frame with a single row
            temp_df = pd.DataFrame([columns])
        
            # append the temporary data frame to the main data frame
            my_df = pd.concat([my_df, temp_df], axis=0)
        
        # reset the index of the data frame
        my_df.iloc[:,0] = my_df.iloc[:,0].astype(int)
        my_df.iloc[:,0] = my_df.iloc[:,0].replace(names_new["old"].to_list(), names_new["new"].to_list())
        my_df = my_df[my_df.iloc[:,0]!= ''] # deleting empty columns if exists
        
        # open a new text file for writing
        with open(file_new, 'w') as f:
            # loop through each row of the dataframe
            for index, row in my_df.iterrows():
                # convert the row to a string and write it to the file
                row = row.dropna()
                row_string = ' '.join(str(x) for x in row.values)
                f.write(row_string + '\n')
    
    except Exception as e:
        print("An error has occured for file: "+file)
        print("Message error gotten from Exception:")
        print(e)
        

classes_path = os.path.join(dataset_input,"labels","classes.txt")

if os.path.isfile(classes_path) and classes_file is not None:
    classes_df = pd.read_csv(classes_path,header=None)
    classes_df.iloc[data["new"],:].to_csv(os.path.join(output_folder,"labels_new","classes.txt"),header=None,index=None) 
    




