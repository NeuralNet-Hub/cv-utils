#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:11:01 2022

@author: henry
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 11:36:02 2022

@author: henry
"""

from matplotlib import pyplot as plt
from clodsa.augmentors.augmentorFactory import createAugmentor
from clodsa.transformers.transformerFactory import transformerGenerator
from clodsa.techniques.techniqueFactory import createTechnique
import cv2


PROBLEM = "instance_segmentation"
ANNOTATION_MODE = "coco"
INPUT_PATH = "train/labels"
GENERATION_MODE = "linear"
OUTPUT_MODE = "coco"
OUTPUT_PATH= "output/"






!mkdir output

augmentor = createAugmentor(PROBLEM,ANNOTATION_MODE,OUTPUT_MODE,GENERATION_MODE,INPUT_PATH,{"outputPath":OUTPUT_PATH})
transformer = transformerGenerator(PROBLEM)


# Rotations
#for angle in [-5,-10,-15]:
#    rotate = createTechnique("rotate", {"angle" : angle})
#    augmentor.addTransformer(transformer(rotate))


#flip = createTechnique("flip",{"flip":1})
#augmentor.addTransformer(transformer(flip))

#shear = createTechnique("shearing", {"a":-0.1})
#augmentor.addTransformer(transformer(shear))


#droput = createTechnique("dropout",{"percentage":0.20})
#augmentor.addTransformer(transformer(droput))

gaussian = createTechnique("gaussian_noise", {"mean" : 5,"sigma":50})
augmentor.addTransformer(transformer(gaussian))







augmentor.applyAugmentation()
























