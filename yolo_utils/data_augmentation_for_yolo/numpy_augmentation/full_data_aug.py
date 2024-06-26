"""
How to run, there are two ways:
    
1) Run with its options
    python full_data_aug.py --horizontal_flip --copy_orig
    python full_data_aug.py --random_scale
    python full_data_aug.py --random_translate
    python full_data_aug.py --rotate
    python full_data_aug.py --random_shear
    python full_data_aug.py --random_HSV
    python full_data_aug.py --random_noise
    python full_data_aug.py --random_bright_contrast
    python full_data_aug.py --sequence
    
    python full_data_aug.py -i ../train -o ../data_out --random_scale --copy_orig --random_translate --rotate --random_shear --random_HSV --random_noise --random_bright_contrast --sequence
    python full_data_aug.py -i ../train -o data_out --random_scale --copy_orig --random_translate --rotate --random_shear --random_HSV --random_bright_contrast --horizontal_flip
    
    
2) Run all data augmentations
    python full_data_aug.py --full -i ../age_folder/train/ -o ../data_out

TIME FOR AUGMENTATION: It takes around 60 minutes in 1000 images.
RAM CONSUMPTION: Approximately 20GB

"""

from data_aug.data_aug import RandomHorizontalFlip, HorizontalFlip, RandomScale, RandomTranslate, \
    RandomRotate, Rotate, RandomShear, RandomHSV, RandomNoise, RandomBrightContrast, Sequence
import cv2 
import numpy as np 
import pandas as pd
import argparse
from tqdm_joblib import tqdm_joblib
import os
from imutils import paths
import shutil
from datetime import datetime
from matplotlib import pyplot as plt
from joblib import Parallel, delayed
import multiprocessing



# parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_out")
parser.add_argument('--horizontal_flip', action='store_true', help='Apply horizontal flip')
parser.add_argument('--random_scale', action='store_true', help='Apply random scale')
parser.add_argument('--random_translate', action='store_true', help='Apply translation')
parser.add_argument('--rotate', action='store_true', help='Apply rotation')
parser.add_argument('--random_shear', action='store_true', help='Apply shear')
parser.add_argument('--random_HSV', action='store_true', help='Apply random HSV values')
parser.add_argument('--random_noise', action='store_true', help='Sum random noise')
parser.add_argument('--random_bright_contrast', action='store_true', help='Modify contrast and brightness')
parser.add_argument('--sequence', action='store_true', help='Apply sequence data augmentation')
parser.add_argument('--copy_orig', action='store_true', help='Save image already loaded by OpenCV')
parser.add_argument('--gray', action='store_true', help='Convert image to grayscale')
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

class augment(object):
    
    def xywhn2xyxy(self, x, w=640, h=640, padw=0, padh=0):
        # Convert nx4 boxes from [c, x, y, w, h] normalized to [x1, y1, x2, y2, c] where xy1=top-left, xy2=bottom-right
        
        y = np.copy(x)
        y[:, 0] = w * (x[:, 1] - x[:, 3] / 2) + padw  # top left x
        y[:, 1] = h * (x[:, 2] - x[:, 4] / 2) + padh  # top left y
        y[:, 2] = w * (x[:, 1] + x[:, 3] / 2) + padw  # bottom right x
        y[:, 3] = h * (x[:, 2] + x[:, 4] / 2) + padh  # bottom right y
        y[:, 4] = x[:, 0]
        return y
    
    
    def xyxy2xywhn(self, x):
        # Convert nx4 boxes from [x1, y1, x2, y2, c] to [c, x, y, w, h] where xy1=top-left, xy2=bottom-right
        dw = 1./self.w
        dh = 1./self.h
        
        
        y = np.copy(x)
        y[:, 1] = ((x[:, 0] + x[:, 2]) / 2)*dw  # x center
        y[:, 2] = ((x[:, 1] + x[:, 3]) / 2)*dh  # y center
        y[:, 3] = (x[:, 2] - x[:, 0]) * dw  # width
        y[:, 4] = (x[:, 3] - x[:, 1]) * dh  # height
        y[:, 0] = x[:, 4]
        return y
    
    
    def save_new_img_txt(self, type_aug, new_bboxes, new_img):
        newfiletxt = os.path.join(dirname_output_label,os.path.splitext(os.path.split(self.filetxt)[1])[0]+"_"+type_aug+".txt")
        newfileimage = os.path.join(dirname_output_image,os.path.splitext(os.path.split(self.fileimage)[1])[0]+"_"+type_aug+self.imgext)
        plt.imsave(newfileimage,new_img)
        new_bboxes = pd.DataFrame(self.xyxy2xywhn(new_bboxes))
        #new_bboxes.iloc[:,0] = new_bboxes.iloc[:,0].astype("int64")
        new_bboxes[new_bboxes.columns[0]] = new_bboxes[new_bboxes.columns[0]].astype("int64")
        if len(new_bboxes):
            new_bboxes.to_csv(newfiletxt,sep=" ",header=False,index=False)
    
    
    
    # Horizontal flip
    def HFlip(self,img,bboxes):
        new_img, new_bboxes = HorizontalFlip()(img.copy(), bboxes.copy())
        self.save_new_img_txt("HorizontalFlip", new_bboxes, new_img)
    
    
    # RandomScale (we use random instead of translate alone in order to get differente values)
    def RScale(self,img,bboxes):
        new_img, new_bboxes = RandomScale(0.5, diff = False)(img.copy(), bboxes.copy())
        self.save_new_img_txt("RandomScale", new_bboxes, new_img)
    
    
    # RandomTranslate (we use random instead of translate alone in order to get differente values)
    def RTrans(self,img,bboxes):
        new_img, new_bboxes = RandomTranslate(0.2, diff = False)(img.copy(), bboxes.copy())
        self.save_new_img_txt("RandomTranslate", new_bboxes, new_img)
    
    
    # Rotate
    def Rot(self,img,bboxes):
        max_angle = 20
        angle_interval = 5
        for angle in [x for x in range(-max_angle,max_angle+angle_interval,angle_interval) if x != 0]: # from -max_angle to max_angle without the angle 0
            new_img, new_bboxes = Rotate(angle)(img.copy(), bboxes.copy())
            self.save_new_img_txt("Rotate_"+str(angle), new_bboxes, new_img)
    
    
    # RandomShear
    def RShear(self,img,bboxes):
        new_img, new_bboxes = RandomShear(0.5)(img.copy(), bboxes.copy())
        self.save_new_img_txt("RandomShear", new_bboxes, new_img)
    
    
    # RandomHSV
    def RHSV(self,img,bboxes):
        new_img, new_bboxes = RandomHSV(100, 100, 100)(img.copy(), bboxes.copy())
        self.save_new_img_txt("RandomHSV", new_bboxes, new_img)
    
    
    # RandomNoise
    def RNoise(self,img,bboxes):
        new_img, new_bboxes = RandomNoise()(img.copy(), bboxes.copy())
        self.save_new_img_txt("RandomNoise", new_bboxes, new_img)
    
    
    # RandomBrightContrast
    def RBright(self,img,bboxes):
        new_img, new_bboxes = RandomBrightContrast(max_contrast=3)(img.copy(), bboxes.copy())
        self.save_new_img_txt("RandomBrightContrast", new_bboxes, new_img)
    
    
    # Sequence (several transformations at the same time)
    def Seq(self,img,bboxes):
        try:
            transforms = Sequence([RandomHorizontalFlip(), RandomScale(0.2, diff = False), RandomTranslate(0.2, diff = False), RandomRotate(20/2),
                                     RandomShear(0.1), RandomHSV(10, 10, 10), RandomBrightContrast(max_contrast=2, max_bright=50)])
            #transforms = Sequence([RandomHSV(40, 40, 30),RandomHorizontalFlip(), RandomScale(), RandomTranslate(), RandomRotate(10), RandomShear()])
            new_img, new_bboxes = transforms(img.copy(), bboxes.copy())
            self.save_new_img_txt("Sequence", new_bboxes, new_img)
            # plt.imshow(draw_rect(new_img, new_bboxes))
            # plt.imshow(draw_rect(img, bboxes))
        except:
            pass
    
    
    # Copying original files
    def Copy(self,img):
        plt.imsave(os.path.join(dirname_output_image,os.path.split(self.fileimage)[1]),img)
        try:
            shutil.copy(self.filetxt,os.path.join(dirname_output_label,os.path.split(self.filetxt)[1]))
        except:
            print("File \'"+os.path.split(self.filetxt)[1]+"\' doesn't have label file")
            
    
    
    # Copying original files
    def Gray(self,img,bboxes):
        new_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
        new_img = np.stack((new_img,)*3, axis=-1)
        new_bboxes = bboxes.copy()
        self.save_new_img_txt("Gray", new_bboxes, new_img)


    def apply(self, fileimage):
        self.fileimage = fileimage
        self.filetxt = os.path.split(fileimage)
        self.filetxt = os.path.join(dataset_input,"labels",self.filetxt[1])
        self.filetxt, self.imgext = os.path.splitext(self.filetxt)
        self.filetxt = self.filetxt + ".txt"
        
        # Reading bboxes. Create empty array in case of background images
        try :
            bboxes = pd.read_table(self.filetxt,header=None,sep=" ")
            bboxes = bboxes.to_numpy()
            #bblabel = 1
        except:
            bboxes = np.empty((0,5)) 
            #bblabel = 0
        
        
        # Reading image and getting dimensions
        img = cv2.imread(fileimage)[:,:,::-1]
        self.h, self.w, c = img.shape
    
        # Transform nomalized coordinates to xyxy coordinates
        bboxes = self.xywhn2xyxy(x = bboxes, w= self.w, h=self.h)
    
        
        # Horizontal flip
        if args.horizontal_flip or args.full:
            self.HFlip(img,bboxes)
     
        # RandomScale (we use random instead of translate alone in order to get differente values)        
        if args.random_scale or args.full:        
            self.RScale(img,bboxes)
        
        # RandomTranslate (we use random instead of translate alone in order to get differente values)
        if args.random_translate or args.full:
            self.RTrans(img,bboxes)
        
        # Rotate
        if args.rotate or args.full:
            self.Rot(img,bboxes)
        
        # RandomShear
        if args.random_shear or args.full:
            self.RShear(img,bboxes)
        
        # RandomHSV
        if args.random_HSV or args.full:
            self.RHSV(img,bboxes)
        
        # RandomNoise
        if args.random_noise or args.full:
            self.RNoise(img,bboxes)
        
        # RandomBrightContrast
        if args.random_bright_contrast or args.full:
            self.RBright(img,bboxes)
        
        # Sequence (several transformations at the same time)
        if args.sequence or args.full:
            self.Seq(img,bboxes)
        
        # Copying original files
        if args.copy_orig or args.full:
            self.Copy(img)
        
        # To gray scale
        if args.gray or args.full:
            self.Gray(img,bboxes)


"""
  _____   _                                      
 |  ___| (_)  _ __    _      __ _   _   _  __  __
 | |_    | | | '_ \  (_)    / _` | | | | | \ \/ /
 |  _|   | | | | | |  _    | (_| | | |_| |  >  < 
 |_|     |_| |_| |_| (_)    \__,_|  \__,_| /_/\_\
                                                 
"""



def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)











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





start = datetime.now()




my_augment = augment()
#my_augment.apply(fileimage)

with tqdm_joblib(desc="Running augmentations for each image", total=len(list_images)) as progress_bar:
    Parallel(n_jobs=multiprocessing.cpu_count())(delayed(my_augment.apply)(fileimage) for fileimage in list_images)
    
print("\nThe process has taken:")
print(datetime.now() - start)
