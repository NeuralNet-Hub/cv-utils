"""


"""

import xmltodict
import pandas as pd
from imutils import paths
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="path_file_in",
                    help="input path for file which contains 'labels'.",
                    default="original/bounding_boxes/labels/train_labels.csv")
parser.add_argument("-o",
                    dest="folder_out",
                    help="new folder where the labels will be saved",
                    default="train/labels")
args = vars(parser.parse_args())


def convert_to_yolo(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


if not os.path.exists(args["folder_out"]):
    os.mkdir(os.path.join(args["folder_out"]))



labels_number = dict()

df_labels = pd.read_csv(args["path_file_in"])

list_files = list(df_labels["filename"].to_list())



for file in tqdm(list_files):

    file_name=file.split(os.path.sep)
    file_name=file_name[len(file_name)-1]
    file_name=file_name.split(".")[0]
    #print(file_name)
    
    df_out=pd.DataFrame({"class":range(0),"xcenter":range(0), "ycenter":range(0), "width":range(0),"height":range(0)})

    doc_df = df_labels.loc[df_labels["filename"]==file,:].reset_index()
        
    w=int(float(doc_df["width"].unique()))
    h=int(float(doc_df["height"].unique()))
    
    
    try:
        for i in range(0,doc_df.shape[0]):
            
            new_doc=doc_df.iloc[i,:]
            label=doc_df.loc[i,"class"]
            
            if label in labels_number.keys():
                label = labels_number[label]
            else:
                labels_number[label] = len(labels_number.keys())
                label = labels_number[label]
            
            xmin=int(float(new_doc["xmin"]))
            xmax=int(float(new_doc["xmax"]))
            ymin=int(float(new_doc["ymin"]))
            ymax=int(float(new_doc["ymax"]))
            
            xcenter,ycenter,w_new,h_new=convert_to_yolo((w,h), (xmin, xmax, ymin, ymax))
            df_out=df_out.append(pd.DataFrame({"class":label,"xcenter":xcenter, "ycenter":ycenter, "width":w_new,"height":h_new},index={0}))
            
        df_out.to_csv(args["folder_out"]+"/"+file_name+".txt",index=False,header=False,sep=" ")
    except Exception as e:
        print(e)
        #print("Image without annotations: "+file_name)
        

with open(os.path.join(args["folder_out"],'classes.txt'), 'w') as f:
    for item in labels_number.keys():
        f.write("%s\n" % item)

