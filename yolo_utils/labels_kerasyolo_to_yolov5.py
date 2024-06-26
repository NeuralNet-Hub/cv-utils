"""
How to run:
python convert_to_yolo_format.py -i data_in -o data_out

IMPORTANT: data_in is the folder of labels

"""



import cv2
import pandas as pd
from imutils import paths
import os
from tqdm import tqdm
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="folder_in",
                    help="input folder which contains XML 'labels'.",
                    default="data_in")
parser.add_argument("-o",
                    dest="folder_out",
                    help="new folder where the labels will be saved")

args = parser.parse_args()
folder_in = args.folder_in

folder_out = args.folder_out if args.folder_out is not None else folder_in


folders_list = os.listdir(folder_in)

if not os.path.exists(folder_out):
    os.mkdir(os.path.join(folder_out))

if not os.path.exists(os.path.join(folder_out,"images")):
    os.mkdir(os.path.join(folder_out,"images"))    

if not os.path.exists(os.path.join(folder_out,"labels")):
    os.mkdir(os.path.join(folder_out,"labels"))    


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





classes = []


for folder in folders_list:

    list_files=list(paths.list_files(os.path.join(folder_in,folder)))
    txt_files = [f for f in list_files if f.endswith('.txt')]
    image_files = [f for f in list_files if f.endswith(tuple(['bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp']))] # include video suffixes
    
    for file in tqdm(image_files):
    
        file_txt = os.path.splitext(file)[0]+".txt"
        
        img = cv2.imread(file)
        h, w, _ = img.shape
    
        # Copy images
        shutil.copy(file,os.path.join(folder_out,"images",os.path.split(file)[1]))
    
        
        # Initialize annotations   
        df_out=pd.DataFrame({"class":range(0),"xcenter":range(0), "ycenter":range(0), "width":range(0),"height":range(0)})
    
        if os.path.isfile(file_txt):
            # Read txt
            try:
                doc = pd.read_csv(file_txt, header = None,sep=" ")
            except Exception as e:
                # Continue to next iteration.
                print("Warning: " + str(e) + ". File: " +os.path.split(file_txt)[1])
                continue
            doc.columns = ["class","xmin","xmax","ymin","ymax"]
            
            # Get annotations
            xmin_list=doc["xmin"]
            xmax_list=doc["xmax"]
            ymin_list=doc["ymin"]
            ymax_list=doc["ymax"]
            
            for (idx, (label, xmin, xmax, ymin, ymax)) in doc.iterrows():
                
                label = 0 if label == -1 else label# Just for FPDS dataset
                xcenter,ycenter,w_new,h_new=convert_to_yolo((w,h), (xmin, xmax, ymin, ymax))
                df_out=df_out.append(pd.DataFrame({"class":label,"xcenter":xcenter, "ycenter":ycenter, "width":w_new,"height":h_new},index={0}))
                
                if not label in classes:
                    classes.append(label)
            
            df_out.to_csv(os.path.join(folder_out,"labels",os.path.split(file_txt)[1]),index=False,header=False,sep=" ")
    
        else:
            print("File does not exist in path: " + file_txt)


classes = ["normal", "fallen"]
classes = pd.DataFrame(classes)
classes.to_csv(os.path.join(folder_out,"labels","classes.txt"),index=False,header=False)
