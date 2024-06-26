#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data augmentation with clodsa: This code makes image augmentation using clodsa.
It has been taken mainly from here: https://github.com/joheras/CLoDSA
and adapted to yolo format. 


1) Run with its options
    python data_aug.py --rotate
    python data_aug.py --translateX
    python data_aug.py --translateY
    python data_aug.py --shear
    python data_aug.py --flip
    python data_aug.py --gamma
    python data_aug.py --equalize
    python data_aug.py --dropout
    python data_aug.py --gaussian
    python data_aug.py --copy_orig
    
    python data_aug.py -i train -o data_out --rotate --translateX --translateY --shear --gamma --equalize --dropout --gaussian --copy_orig --flip
    
    
2) Run all data augmentations
    python data_aug.py  --full -i train -o data_out


TIME FOR AUGMENTATION: It takes around 30 minutes in 1000 images.
RAM CONSUMPTION: Approximately 15GB


"""

# Clodsa functions
from clodsa.augmentors.augmentorFactory import createAugmentor
from clodsa.transformers.transformerFactory import transformerGenerator
from clodsa.techniques.techniqueFactory import createTechnique

# Common libraries
from datetime import datetime
import os
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="directory which contains a file called \'annotations.json\' with all the annotations. The file must be located in the same folder as images",
                    default="train")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_out")

parser.add_argument('--rotate', action='store_true', help='Apply rotation from -15 degrees to 15 degrees')
parser.add_argument('--translateX', action='store_true', help='Apply translation in X axis')
parser.add_argument('--translateY', action='store_true', help='Apply translation in X axis')
parser.add_argument('--shear', action='store_true', help='Apply shear for a=-0.2 and a=0.2')
parser.add_argument('--flip', action='store_true', help='Apply horizontal flip')
parser.add_argument('--gamma', action='store_true', help='Apply gamma correction (color changes a little bit, 0 < gamma < 2.5)')
parser.add_argument('--elastic', action='store_true', help='Apply elastic deformation (segments fade a little)')
parser.add_argument('--equalize', action='store_true', help='Applies histogram equalization to the image.')
parser.add_argument('--dropout', action='store_true', help='Sets some pixels in the image to zero (add black dots).')
parser.add_argument('--gaussian', action='store_true', help='Add gaussian noise with mean: 5 and sigma: 50. (random dots)')
parser.add_argument('--copy-orig', action='store_true', help='If you want to copy the original image into the new folder (recommended)')
parser.add_argument('--average-blurring', action='store_true', help='Apply average blurring to image (not aggresive blur)')
parser.add_argument('--full', action='store_true', help='Apply all data augmentations')

args = parser.parse_args()




def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)


"""
# Techniques list that can be applied
Techniques = {
    "average_blurring" : averageBlurringAugmentationTechnique,
    "bilateral_blurring" : bilateralBlurringAugmentationTechnique,
    "blurring" : blurringAugmentationTechnique,
    "change_to_hsv" : changeToHSVAugmentationTechnique,
    "change_to_lab" : changeToLABAugmentationTechnique,
    "crop" : cropAugmentationTechnique,
    "cropSize" : cropSizeAugmentationTechnique,
    "dropout" : dropoutAugmentationTechnique,
    "elastic" : elasticTransformAugmentationTechnique,
    "equalize_histogram" : equalizeHistogramAugmentationTechnique,
    "flip" : flipAugmentationTechnique,
    "gamma" : gammaCorrectionAugmentationTechnique,
    "gaussian_blur": gausianBlurringAugmentationTechnique,
    "gaussian_noise": gaussianNoiseAugmentationTechnique,
    "invert": invertAugmentationTechnique,
    "median_blur": medianBlurringAugmentationTechnique,
    "none":  noneAugmentationTechnique,
    "raise_blue":  raiseBlueAugmentationTechnique,
    "raise_green":raiseGreenAugmentationTechnique,
    "raise_hue": raiseHueAugmentationTechnique,
    "raise_red": raiseRedAugmentationTechnique,
    "raise_saturation": raiseSaturationAugmentationTechnique,
    "raise_value":raiseValueAugmentationTechnique,
    "resize": resizeAugmentationTechnique,
    "rotate": rotateAugmentationTechnique,
    "salt_and_pepper":saltAndPepperNoiseAugmentationTechnique,
    "sharpen":sharpenAugmentationTechnique,
    "shift_channel":shiftChannelAugmentationTechnique,
    "shearing": shearingAugmentationTechnique,
    "translation": translationAugmentationTechnique
}
"""


# Setting the inputs. You can change this parameters according to the annotations, see here: https://github.com/joheras/CLoDSA
PROBLEM = "instance_segmentation"
ANNOTATION_MODE = "coco"
INPUT_PATH = args.dataset_input
GENERATION_MODE = "linear"
OUTPUT_MODE = "coco"
OUTPUT_PATH= args.dataset_output



mkdir_p(OUTPUT_PATH)


# Set the starting time for getting the control
start = datetime.now()
print(str(start)+": Process has started...")
print("Following data augmentations will be done:")
print(args)


# Set the Augmentor class
augmentor = createAugmentor(PROBLEM,ANNOTATION_MODE,OUTPUT_MODE,GENERATION_MODE,INPUT_PATH,{"outputPath":OUTPUT_PATH+os.path.sep})
transformer = transformerGenerator(PROBLEM)


# Average blurring
if args.average_blurring or args.full:

    test = createTechnique("average_blurring",{})
    augmentor.addTransformer(transformer(test))


# Rotations from -15 to 15
if args.rotate or args.full:

    # Rotations
    for angle in [-15,-10,-5,5,10,15]:
        rotate = createTechnique("rotate", {"angle" : angle})
        augmentor.addTransformer(transformer(rotate))

# Horizontal Flip
if args.flip or args.full:

    flip = createTechnique("flip",{"flip":1}) # 1 means vertical flip
    augmentor.addTransformer(transformer(flip))


# Translate in X
if args.translateX or args.full:

    for value in [-30,30]:
        translateX = createTechnique("translation", {"x":value})
        augmentor.addTransformer(transformer(translateX))
   
     
# Translate in Y
if args.translateY or args.full:

    for value in [-30,30]:
        translateY = createTechnique("translation", {"y":value})
        augmentor.addTransformer(transformer(translateY))


# Shearing (deforming a little the image)
if args.shear or args.full:

    for value in [-0.2,0.2]:
        shear = createTechnique("shearing", {"a":value})
        augmentor.addTransformer(transformer(shear))
    
    
# Gamma correction technique 0 < gamma < 2.5
if args.gamma or args.full:
    gamma = createTechnique("gamma",{"gamma":1.5})
    augmentor.addTransformer(transformer(gamma))


# Elastic deformation
"""
Doesn't work in yolo segmentation
if args.elastic or args.full:
    elastic = createTechnique("elastic",{"alpha":1,"sigma":0.05}) # the higher the alpha the more aggresive
    augmentor.addTransformer(transformer(elastic))
"""

# Equalize histogram
if args.equalize or args.full:
    equalize = createTechnique("equalize_histogram",{})
    augmentor.addTransformer(transformer(equalize))


# Dropout
if args.dropout or args.full:
    dropout = createTechnique("dropout",{"percentage":0.20})
    augmentor.addTransformer(transformer(dropout))
    
    

# Gaussian noise
if args.gaussian or args.full:
    gaussian = createTechnique("gaussian_noise", {"mean" : 5,"sigma":50})
    augmentor.addTransformer(transformer(gaussian))
    

# Copy orig
if args.copy_orig or args.full:
    # Rotate 0 degrees
    copy_orig = createTechnique("rotate", {"angle" : 0})
    augmentor.addTransformer(transformer(copy_orig))

    




# Finally run the augmentor, unfortunately it is not possible to see the progress

augmentor.applyAugmentation()
print("\nThe process has taken:")
print(datetime.now() - start)







