"""
How to run:
python convert_to_yolo_format.py -i data_in -o data_out

IMPORTANT: data_in is the folder of labels

"""



import xmltodict
import pandas as pd
from imutils import paths
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="folder_in",
                    help="input folder which contains XML 'labels'.",
                    default="data_in")
parser.add_argument("-o",
                    dest="folder_out",
                    help="new folder where the labels will be saved",
                    default="data_out")
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

#args["folder_in"] = "../../yolo/datasets/dog_dataset/annotation/Annotation/n02085620-Chihuahua/"

list_files=list(paths.list_files(args["folder_in"]))

labels_number = dict()


for file in tqdm(list_files):

    file_name=file.split(os.path.sep)
    file_name=file_name[len(file_name)-1]
    file_name=file_name.split(".")[0]
    #print(file_name)
    
    df_out=pd.DataFrame({"class":range(0),"xcenter":range(0), "ycenter":range(0), "width":range(0),"height":range(0)})

    with open(file) as fd:
        doc = xmltodict.parse(fd.read())
        
    
    w=int(float(doc["annotation"]["size"]["width"]))
    h=int(float(doc["annotation"]["size"]["height"]))
    
    one_length=True
    try:
        label=doc["annotation"]["object"]["name"]
    except:
        one_length=False
    
    if one_length:
        label=doc["annotation"]["object"]["name"]
        
        if label in labels_number.keys():
            label = labels_number[label]
        else:
            labels_number[label] = len(labels_number.keys())
            label = labels_number[label]
        
        xmin=int(float(doc["annotation"]["object"]["bndbox"]["xmin"]))
        xmax=int(float(doc["annotation"]["object"]["bndbox"]["xmax"]))
        ymin=int(float(doc["annotation"]["object"]["bndbox"]["ymin"]))
        ymax=int(float(doc["annotation"]["object"]["bndbox"]["ymax"]))
        
        
        xcenter,ycenter,w_new,h_new=convert_to_yolo((w,h), (xmin, xmax, ymin, ymax))
        df_out= pd.concat([df_out, pd.DataFrame({"class":label,"xcenter":xcenter, "ycenter":ycenter, "width":w_new,"height":h_new},index=[0])])
        
        df_out.to_csv(args["folder_out"]+"/"+file_name+".txt",index=False,header=False,sep=" ")
    
    else:
        try:
            for i in range(len(doc["annotation"]["object"])):
                
                new_doc=doc["annotation"]["object"][i]
                label=doc["annotation"]["object"][i]["name"]
                
                if label in labels_number.keys():
                    label = labels_number[label]
                else:
                    labels_number[label] = len(labels_number.keys())
                    label = labels_number[label]
                
                
                xmin=int(float(new_doc["bndbox"]["xmin"]))
                xmax=int(float(new_doc["bndbox"]["xmax"]))
                ymin=int(float(new_doc["bndbox"]["ymin"]))
                ymax=int(float(new_doc["bndbox"]["ymax"]))
                
                xcenter,ycenter,w_new,h_new=convert_to_yolo((w,h), (xmin, xmax, ymin, ymax))
                df_out= pd.concat([df_out, pd.DataFrame({"class":label,"xcenter":xcenter, "ycenter":ycenter, "width":w_new,"height":h_new},index=[0])])
                
            df_out.to_csv(args["folder_out"]+"/"+file_name+".txt",index=False,header=False,sep=" ")
        except:
            print("Image without annotations: "+file_name)
        

with open(os.path.join(args["folder_out"],'classes.txt'), 'w') as f:
    for item in labels_number.keys():
        f.write("%s\n" % item)

