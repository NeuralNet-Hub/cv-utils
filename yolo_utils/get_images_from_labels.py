

import os
import argparse
import shutil
from tqdm import tqdm
from imutils import paths
import numpy as np

# parsing
parser = argparse.ArgumentParser()
parser.add_argument("--image-path",
                    dest="images",
                    help="input path images",
                    default="data_in")
parser.add_argument("--labels-path",
                    dest="labels",
                    help="input path with labels and images",
                    default="data_in")
parser.add_argument("--output",
                    dest="image_folder_out",
                    help="path out images",
                    default="new_images")
args = parser.parse_args()

dirname_input_image  = args.image_path
dirname_input_label  = args.labels_path
image_folder_out = args.output

def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

mkdir_p(image_folder_out)



my_txts = np.array(os.listdir(dirname_input_label))[np.where([file.endswith(".txt") for file in os.listdir(dirname_input_label)])]
my_images = list(paths.list_images(dirname_input_image))



for txt0 in tqdm(my_txts):
    
    basename_txt = os.path.splitext(os.path.basename(txt0))[0]
    
    
    jpg_file_in = os.path.join(dirname_input_image, basename_txt+".jpg")
    jpg_file_out = os.path.join(image_folder_out, basename_txt+".jpg")
    
    try:
        #shutil.copy(jpg_file_in,jpg_file_out)
        shutil.move(jpg_file_in,jpg_file_out)
    except Exception as e:
        print(e)
        #os.remove(os.path.join(dirname_input_label,txt0))
        
