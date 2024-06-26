"""
It will return in a folder random frames according to a prob parameter

How to run:
python from_video_to_frame.py -i data_in -o data_out -prob 0.9
    

"""

import cv2
from imutils import paths
import os
import numpy as np
import argparse
from tqdm import tqdm



# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory where videos are storage, frames will be gotten from all videos of this folder",
                    default="data_in")

parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory where frames will be stored",
                    default="data_out")


parser.add_argument("-prob",
                    type=float,
                    dest="prob",
                    help="probability to save frame (default 0.5)",
                    default=0.5)


args = parser.parse_args()

#data_in = "data_in"
#data_out = "data_out"
data_in = args.dataset_input
data_out = args.dataset_output
prob = args.prob

if not os.path.isdir(data_out):
    os.makedirs(data_out)

list_files=list(paths.list_files(data_in))

for file in list_files:
    
    print("Extracting frame from file "+file)
    folder_name, file_name = os.path.split(file)
    folder_name = os.path.split(folder_name)[1]
    file_name = os.path.splitext(file_name)[0]

    vs = cv2.VideoCapture(file)
    total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    
        
    for i in tqdm(range(0,total_frames)):
       	# read the next frame from the file
       	(grabbed, frame) = vs.read()
          
    
       	# if the frame was not grabbed, then we have reached the end
       	# of the stream
       	if not grabbed:
       		break
        
        #frame=cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
        
        if np.random.uniform(0,1) > (1-prob):
            
            #print("Número de frame guardado: "+str(i))
            cv2.imwrite(os.path.join(data_out,folder_name+"_"+file_name+"_frame_"+str(i)+".jpg"),frame)
