#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:51:02 2024

@author: henry
"""
import os
import cv2
import base64
import json
from ultralytics import YOLO
from imutils import paths

# Load a pretrained YOLOv8n-seg Segment model
model = YOLO('yolov8x-seg.pt')


list_images = paths.list_images("/home/henry/Projects/CV_solutions/ultralytics/datasets/roboflow_synth/images/")

for path in list_images:
    # Run inference on an image
    results = model(path,
                    classes=[0],
                    conf=0.6,
                    imgsz=1280,
                    retina_masks=True)  # results list
    
    # View results
    for r in results:
        points = []
        
        _, buffer = cv2.imencode('.jpg', r.orig_img)
        base64_image = base64.b64encode(buffer).decode('utf-8')
        
        converted_data = {
            "version": "5.4.1",
            "flags": {},
            "shapes": [],
            "imagePath": r.path,
            "imageData": base64_image,
            "imageHeight": r.orig_shape[0],
            "imageWidth": r.orig_shape[1]
        }
        
        if r.masks is not None:
            for mask in r.masks:
                
                array = mask.xy[0]
        
                shapes = {
                        "label": "person",
                        "points": [[float(x), float(y)] for x, y in array],
                        "group_id": None,
                        "description": "",
                        "shape_type": "polygon",
                        "flags": {},
                        "mask": None
                    }
        
                converted_data["shapes"].append(shapes)
            
            with open(os.path.splitext(r.path)[0]+".json", 'w') as f:
                json.dump(converted_data, f, indent=2)
    
    
    
    