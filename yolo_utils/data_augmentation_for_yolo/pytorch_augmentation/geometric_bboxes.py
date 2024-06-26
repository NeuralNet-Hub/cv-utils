"""
Data augmentation with pytorch: This code makes image augmentation using pytorch.
It has been taken mainly from here: https://github.com/Jasonlee1995/AutoAugment_Detection.git
and adapted to yolo format. 


1) Run with its options
    python geometric_bboxes.py --rotate
    python geometric_bboxes.py --translateX
    python geometric_bboxes.py --translateY
    python geometric_bboxes.py --shearX
    python geometric_bboxes.py --shearY
    python geometric_bboxes.py --flip
    python geometric_bboxes.py --full
    
    python geometric_bboxes.py -i ../train -o ../data_out --rotate --translateX --translateY --shearX --shearY
    python geometric_bboxes.py -i ../train -o ../data_out --rotate --translateX --translateY --shearX --shearY --flip
    
    
2) Run all data augmentations
    python geometric_bboxes.py  --full -i ../age_folder/train/ -o ../data_out


TIME FOR AUGMENTATION: It takes around 50 minutes in 1000 images.
RAM CONSUMPTION: Approximately 10GB


"""




import augmentation, torch
from datetime import datetime
import pandas as pd
import argparse
from tqdm import tqdm
import os
from imutils import paths
import shutil
from PIL import Image, ImageOps
from multiprocessing import Process


# Ignore Warning
import warnings
warnings.filterwarnings(action='ignore')


parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_out")

parser.add_argument('--rotate', action='store_true', help='Apply rotation')
parser.add_argument('--translateX', action='store_true', help='Apply translation in X axis')
parser.add_argument('--translateY', action='store_true', help='Apply translation in X axis')
parser.add_argument('--shearX', action='store_true', help='Apply shear in X axis')
parser.add_argument('--shearY', action='store_true', help='Apply shear in Y axis')
parser.add_argument('--flip', action='store_true', help='Apply horizontal flip')
parser.add_argument('--full', action='store_true', help='Apply all data augmentations')



args = parser.parse_args()



"""
  ___           _          _                                      
 |_ _|  _ __   (_)   ___  (_)   ___    _      __ _   _   _  __  __
  | |  | '_ \  | |  / __| | |  / _ \  (_)    / _` | | | | | \ \/ /
  | |  | | | | | | | (__  | | | (_) |  _    | (_| | | |_| |  >  < 
 |___| |_| |_| |_|  \___| |_|  \___/  (_)    \__,_|  \__,_| /_/\_\
                                                                  
No tengo idea de cómo putas poner esto en una librería y que tome las variables globales que le paso

"""


def xywhn2xyxy(x, w=640, h=640, padw=0, padh=0):
    # Convert nx4 boxes from [c, x, y, w, h] normalized to [x1, y1, x2, y2], c where xy1=top-left, xy2=bottom-right
    
    y = x.clone()
    y[:, 0] = w * (x[:, 1] - x[:, 3] / 2) + padw  # top left x
    y[:, 1] = h * (x[:, 2] - x[:, 4] / 2) + padh  # top left y
    y[:, 2] = w * (x[:, 1] + x[:, 3] / 2) + padw  # bottom right x
    y[:, 3] = h * (x[:, 2] + x[:, 4] / 2) + padh  # bottom right y
    #y[:, 4] = x[:, 0]
    y = y[:,0:4]
    return y, x[:, 0]


def xyxy2xywhn(x, c):
    # Convert nx4 boxes from [x1, y1, x2, y2] to [c, x, y, w, h] where xy1=top-left, xy2=bottom-right
    
    dw = 1./w
    dh = 1./h
    
    
    y = torch.empty(x.shape[0],5)
    y[:, 1] = ((x[:, 0] + x[:, 2]) / 2)*dw  # x center
    y[:, 2] = ((x[:, 1] + x[:, 3]) / 2)*dh  # y center
    y[:, 3] = (x[:, 2] - x[:, 0]) * dw  # width
    y[:, 4] = (x[:, 3] - x[:, 1]) * dh  # height
    y[:, 0] = c
    return y





def save_new_img_txt(type_aug, new_bboxes, new_img, labels):
    newfiletxt = os.path.join(dirname_output_label,os.path.splitext(os.path.split(filetxt)[1])[0]+"_"+type_aug+".txt")
    newfileimage = os.path.join(dirname_output_image,os.path.splitext(os.path.split(fileimage)[1])[0]+"_"+type_aug+imgext)
    new_img.save(newfileimage)
    new_bboxes = pd.DataFrame(xyxy2xywhn(new_bboxes,labels).numpy())
    new_bboxes.iloc[:,0] = new_bboxes.iloc[:,0].astype("int64")
    if len(new_bboxes):
        new_bboxes.to_csv(newfiletxt,sep=" ",header=False,index=False)


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

aug_list = [augmentation.Rotate_Only_BBoxes(3, -5, minus=False), augmentation.Rotate_Only_BBoxes(3, 5, minus=False), 
            augmentation.TranslateX_Only_BBoxes(3, -5, minus=False), augmentation.TranslateX_Only_BBoxes(3, 5, minus=False),
            augmentation.TranslateY_Only_BBoxes(3, -5, minus=False), augmentation.TranslateY_Only_BBoxes(3, 5, minus=False),
            augmentation.ShearX_Only_BBoxes(3, -0.2, minus=False), augmentation.ShearX_Only_BBoxes(3, 0.2, minus=False),
            augmentation.ShearY_Only_BBoxes(3, -0.2, minus=False), augmentation.ShearY_Only_BBoxes(3, 0.2, minus=False), 
            augmentation.Flip_Only_BBoxes(3)]

title_list = ['Rotate_Only_BBoxes_-5', 'Rotate_Only_BBoxes_5',
              'TranslateX_Only_BBoxes_-30', 'TranslateX_Only_BBoxes_30',
              'TranslateY_Only_BBoxes_-30', 'TranslateY_Only_BBoxes_30',
              'ShearX_Only_BBoxes_-0.2', 'ShearX_Only_BBoxes_0.2',
              'ShearY_Only_BBoxes_-0.2', 'ShearY_Only_BBoxes_0.2',
              'Flip_Only_BBoxes']


def addfunc(i):
    def addn(img,bboxes):
        new_img, new_bboxes = aug_list[i](img, bboxes)
        save_new_img_txt(title_list[i], new_bboxes, new_img, labels)
        return
    return addn


for i in range(0,len(title_list)):
    globals()['func{}'.format(i+1)] = addfunc(i)



"""
  _____   _                                      
 |  ___| (_)  _ __    _      __ _   _   _  __  __
 | |_    | | | '_ \  (_)    / _` | | | | | \ \/ /
 |  _|   | | | | | |  _    | (_| | | |_| |  >  < 
 |_|     |_| |_| |_| (_)    \__,_|  \__,_| /_/\_\
                                                 
"""






dataset_input = args.dataset_input
dataset_output = args.dataset_output

dirname_input_image  = os.path.join( dataset_input  , "images" )
dirname_input_label  = os.path.join( dataset_input  , "labels" )
dirname_output_image = os.path.join( dataset_output , "images" )
dirname_output_label = os.path.join( dataset_output , "labels" )



mkdir_p(dataset_output)
mkdir_p(dirname_output_image)
mkdir_p(dirname_output_label)

list_images = list(paths.list_images(dirname_input_image))

# Copy classes file before start
try:
    shutil.copy(os.path.join(dirname_input_label,"classes.txt"),os.path.join(dirname_output_label,"classes.txt"))
except:
    print("WARNING: There is no 'classes.txt' file in labels folder")




list_images = list(paths.list_images(dirname_input_image))


start = datetime.now()


for fileimage in tqdm(list_images):
    #print(os.path.split(fileimage)[1])
    # Getting txt file name
    filetxt = os.path.split(fileimage)
    filetxt = os.path.join(dataset_input,"labels",filetxt[1])
    filetxt, imgext = os.path.splitext(filetxt)
    filetxt = filetxt + ".txt"
    
    # Reading bboxes. Create empty array in case of background images
    try :
        bboxes = pd.read_table(filetxt,header=None,sep=" ")
        bboxes = torch.FloatTensor(bboxes.to_numpy())
        #bblabel = 1
    except:
        #bboxes = np.empty((0,5)) 
        bboxes = torch.empty((0, 5))
        #torch.zeros_like(bboxes)
        #bblabel = 0
        
    if bboxes.numel(): # Just run this in case the image has bboxes
    
        img = Image.open(fileimage).convert('RGB')
        img = ImageOps.exif_transpose(img)
        
        w, h = img.size
    
    
        # Transform nomalized coordinates to xyxy coordinates
        bboxes, labels = xywhn2xyxy(x = bboxes, w= w, h=h)
        
        # https://stackoverflow.com/questions/18864859/python-executing-multiple-functions-simultaneously
        
        if args.rotate or args.full:
            p1 = Process(target = func1, args = (img,bboxes))
            p1.start()
            p2 = Process(target = func2, args = (img,bboxes))
            p2.start()
        
        
        if args.translateX or args.full:
            p3 = Process(target = func3, args = (img,bboxes))
            p3.start()
            p4 = Process(target = func4, args = (img,bboxes))
            p4.start()
            
            
        if args.translateY or args.full:
            p5 = Process(target = func5, args = (img,bboxes))
            p5.start()
            p6 = Process(target = func6, args = (img,bboxes))
            p6.start()
        
        
        if args.shearX or args.full:
            p7 = Process(target = func7, args = (img,bboxes))
            p7.start()
            p8 = Process(target = func8, args = (img,bboxes))
            p8.start()
            
        
        if args.shearY or args.full:
            p9 = Process(target = func9, args = (img,bboxes))
            p9.start()
            p10 = Process(target = func10, args = (img,bboxes))
            p10.start()
        
        if args.flip or args.full:
            p11 = Process(target = func11, args = (img,bboxes))
            p11.start()

print("\nThe process has taken:")
print(datetime.now() - start)
