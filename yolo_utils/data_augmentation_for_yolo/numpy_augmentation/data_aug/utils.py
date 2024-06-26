"""
utils.py: This code contains auxiliar functions like xywhn2xyxy, xyxy2xywhn, save_new_img_txt, mkdir_p that help to transform bboxes an other tasks.

The code also contains functions for data augmentation in multiprocessing

"""

import os
import numpy as np
from data_aug.data_aug import RandomHorizontalFlip, HorizontalFlip, RandomScale, RandomTranslate, \
    RandomRotate, Rotate, RandomShear, RandomHSV, RandomNoise, RandomBrightContrast, Sequence
from matplotlib import pyplot as plt
import pandas as pd
import shutil





def xywhn2xyxy(x, w=640, h=640, padw=0, padh=0):
    # Convert nx4 boxes from [c, x, y, w, h] normalized to [x1, y1, x2, y2, c] where xy1=top-left, xy2=bottom-right
    
    y = np.copy(x)
    y[:, 0] = w * (x[:, 1] - x[:, 3] / 2) + padw  # top left x
    y[:, 1] = h * (x[:, 2] - x[:, 4] / 2) + padh  # top left y
    y[:, 2] = w * (x[:, 1] + x[:, 3] / 2) + padw  # bottom right x
    y[:, 3] = h * (x[:, 2] + x[:, 4] / 2) + padh  # bottom right y
    y[:, 4] = x[:, 0]
    return y


def xyxy2xywhn(x):
    # Convert nx4 boxes from [x1, y1, x2, y2, c] to [c, x, y, w, h] where xy1=top-left, xy2=bottom-right
    dw = 1./w
    dh = 1./h
    
    
    y = np.copy(x)
    y[:, 1] = ((x[:, 0] + x[:, 2]) / 2)*dw  # x center
    y[:, 2] = ((x[:, 1] + x[:, 3]) / 2)*dh  # y center
    y[:, 3] = (x[:, 2] - x[:, 0]) * dw  # width
    y[:, 4] = (x[:, 3] - x[:, 1]) * dh  # height
    y[:, 0] = x[:, 4]
    return y


def save_new_img_txt(type_aug, new_bboxes, new_img):
    newfiletxt = os.path.join(dirname_output_label,os.path.splitext(os.path.split(filetxt)[1])[0]+"_"+type_aug+".txt")
    newfileimage = os.path.join(dirname_output_image,os.path.splitext(os.path.split(fileimage)[1])[0]+"_"+type_aug+imgext)
    plt.imsave(newfileimage,new_img)
    new_bboxes = pd.DataFrame(xyxy2xywhn(new_bboxes))
    new_bboxes.iloc[:,0] = new_bboxes.iloc[:,0].astype("int64")
    if len(new_bboxes):
        new_bboxes.to_csv(newfiletxt,sep=" ",header=False,index=False)




def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)



# Horizontal flip
def HFlip():
    new_img, new_bboxes = HorizontalFlip()(img.copy(), bboxes.copy())
    save_new_img_txt("HorizontalFlip", new_bboxes, new_img)


# RandomScale (we use random instead of translate alone in order to get differente values)
def RScale():
    new_img, new_bboxes = RandomScale(0.5, diff = False)(img.copy(), bboxes.copy())
    save_new_img_txt("RandomScale", new_bboxes, new_img)


# RandomTranslate (we use random instead of translate alone in order to get differente values)
def RTrans():
    new_img, new_bboxes = RandomTranslate(0.2, diff = False)(img.copy(), bboxes.copy())
    save_new_img_txt("RandomTranslate", new_bboxes, new_img)


# Rotate
def Rot():
    max_angle = 20
    angle_interval = 4
    for angle in [x for x in range(-max_angle,max_angle+angle_interval,angle_interval) if x != 0]: # from -max_angle to max_angle without the angle 0
        new_img, new_bboxes = Rotate(angle)(img.copy(), bboxes.copy())
        save_new_img_txt("Rotate_"+str(angle), new_bboxes, new_img)


# RandomShear
def RShear():
    new_img, new_bboxes = RandomShear(0.5)(img.copy(), bboxes.copy())
    save_new_img_txt("RandomShear", new_bboxes, new_img)


# RandomHSV
def RHSV():
    new_img, new_bboxes = RandomHSV(100, 100, 100)(img.copy(), bboxes.copy())
    save_new_img_txt("RandomHSV", new_bboxes, new_img)


# RandomNoise
def RNoise():
    new_img, new_bboxes = RandomNoise()(img.copy(), bboxes.copy())
    save_new_img_txt("RandomNoise", new_bboxes, new_img)


# RandomBrightContrast
def RBright():
    new_img, new_bboxes = RandomBrightContrast(max_contrast=3, max_bright=100)(img.copy(), bboxes.copy())
    save_new_img_txt("RandomBrightContrast", new_bboxes, new_img)


# Sequence (several transformations at the same time)
def Seq():
    try:
        transforms = Sequence([RandomHorizontalFlip(), RandomScale(0.2, diff = False), RandomTranslate(0.2, diff = False), RandomRotate(20/2),
                                 RandomShear(0.1), RandomHSV(10, 10, 10), RandomBrightContrast(max_contrast=2, max_bright=50)])
        #transforms = Sequence([RandomHSV(40, 40, 30),RandomHorizontalFlip(), RandomScale(), RandomTranslate(), RandomRotate(10), RandomShear()])
        new_img, new_bboxes = transforms(img.copy(), bboxes.copy())
        save_new_img_txt("Sequence", new_bboxes, new_img)
        # plt.imshow(draw_rect(new_img, new_bboxes))
        # plt.imshow(draw_rect(img, bboxes))
        print("HERE")
    except:
        pass


# Copying original files
def Copy():
    plt.imsave(os.path.join(dirname_output_image,os.path.split(fileimage)[1]),img)
    try:
        shutil.copy(filetxt,os.path.join(dirname_output_label,os.path.split(filetxt)[1]))
    except:
        print("File \'"+os.path.split(filetxt)[1]+"\' doesn't have label file")













