#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:50:02 2022

@author: henry
"""

# For plate reader and communication
from easyocr import Reader
import cv2
import os
import numpy as np
from imutils import paths

def put_box_label(im, box, label='', lw = 2, color=(0, 255, 0), txt_color=(255, 255, 255)):
    # Add one xyxy box to image with label
    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    cv2.rectangle(im, p1, p2, color, thickness=lw, lineType=cv2.LINE_AA)
    if label:
        tf = max(lw - 1, 1)  # font thickness
        w, h = cv2.getTextSize(label, 0, fontScale=lw / 3, thickness=tf)[0]  # text width, height
        outside = p1[1] - h - 3 >= 0  # label fits outside box
        p2 = p1[0] + w - int(w/4), p1[1] - h - 3 if outside else p1[1] + h + 3
        cv2.rectangle(im, p1, p2, (0, 0, 0), -1, cv2.LINE_AA)  # filled
        cv2.putText(im, label, (p1[0]+7, p1[1] - 7 if outside else p1[1] + h + 2), 5, lw / 3.5, txt_color,
                    thickness=tf, lineType=cv2.LINE_AA)


reader = Reader(["en"], gpu = False)

# ================================================================================ #
#  _               _              _      __           _       _               
# | |       __ _  | |__     ___  | |    / _|   ___   | |   __| |   ___   _ __ 
# | |      / _` | | '_ \   / _ \ | |   | |_   / _ \  | |  / _` |  / _ \ | '__|
# | |___  | (_| | | |_) | |  __/ | |   |  _| | (_) | | | | (_| | |  __/ | |   
# |_____|  \__,_| |_.__/   \___| |_|   |_|    \___/  |_|  \__,_|  \___| |_|   
# ================================================================================ #
                                                                             
list_images= list(paths.list_images("jalon"))
for file in list_images:
    img_bgr = cv2.imread(file)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    # From opencv
    lptext = reader.readtext(img_rgb)
    print(lptext)
    for box, label, conf in lptext:
        conf = np.round(conf,3)
        box_new = box[0][0], box[0][1], box[2][0], box[2][1]
        put_box_label(img_bgr,box_new,label+' conf: '+str(conf),lw=5)
    cv2.imwrite(os.path.splitext(file)[0]+'_opencv'+os.path.splitext(file)[1], img_bgr)

# ==================================================== #
#  _____                                 __   _   _        
# |  ___|  _ __    ___    _ __ ___      / _| (_) | |   ___ 
# | |_    | '__|  / _ \  | '_ ` _ \    | |_  | | | |  / _ \
# |  _|   | |    | (_) | | | | | | |   |  _| | | | | |  __/
# |_|     |_|     \___/  |_| |_| |_|   |_|   |_| |_|  \___|
# ==================================================== #                       


#lptext = reader.readtext(plate_square) 
file = "MicrosoftTeams-image (2).jpg"
file = "jalon/20230124_044332(p. m.)___[org].jpg"
img_bgr = cv2.imread(file)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# From opencv
lptext = reader.readtext(img_rgb)
print(lptext)
for box, label, conf in lptext:
    conf = np.round(conf,3)
    box_new = box[0][0], box[0][1], box[2][0], box[2][1]
    put_box_label(img_bgr,box_new,label+' conf: '+str(conf))
cv2.imwrite(os.path.splitext(file)[0]+'_file'+os.path.splitext(file)[1], img_bgr)


# ================================================================================ #
#  _____                                                                          
# |  ___|  _ __    ___    _ __ ___      _ __    _   _   _ __ ___    _ __    _   _ 
# | |_    | '__|  / _ \  | '_ ` _ \    | '_ \  | | | | | '_ ` _ \  | '_ \  | | | |
# |  _|   | |    | (_) | | | | | | |   | | | | | |_| | | | | | | | | |_) | | |_| |
# |_|     |_|     \___/  |_| |_| |_|   |_| |_|  \__,_| |_| |_| |_| | .__/   \__, |
#                                                                  |_|      |___/ 
# ================================================================================ #



# From file
lptext = reader.readtext(file)
print(lptext)
for box, label, conf in lptext:
    conf = np.round(conf,3)
    box_new = box[0][0], box[0][1], box[2][0], box[2][1]
    put_box_label(img_bgr,box_new,label+' conf: '+str(conf))
cv2.imwrite(os.path.splitext(file)[0]+'_file'+os.path.splitext(file)[1], img_bgr)

