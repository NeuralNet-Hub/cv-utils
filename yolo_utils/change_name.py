from imutils import paths
from tqdm import tqdm
import shutil
import os
import numpy as np

list_files=list(paths.list_files("yourfolderin"))
out_path = "yourfolderout"

for file in tqdm(list_files):
    
    _, file_name = os.path.split(file)
    file_name=list(os.path.splitext(file_name))
    file_name[0]=file_name[0]+"_other"
    file_name = os.path.join(out_path,"".join(file_name))


    print(file_name)
    

    shutil.copy(file,file_name)
    #os.remove(file)
    
