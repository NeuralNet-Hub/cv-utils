#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:42:52 2022

@author: henry
"""

'''
Created on Aug 18, 2021

@author: xiaosonh
'''
import os
import sys
import argparse
import shutil
import math
from collections import OrderedDict

import json
import cv2
import PIL.Image
from imutils import paths
  
from sklearn.model_selection import train_test_split
from labelme import utils
from tqdm import tqdm
from joblib import Parallel, delayed
import pandas as pd

class Labelme2YOLO(object):
    
    def __init__(self, json_dir, number_cores, output_dir, classes_file):
        self._json_dir = json_dir
        self.number_cores = number_cores
        self.output_dir = output_dir
        self.classes_file = classes_file
        self._label_id_map = self._get_label_id_map(self._json_dir)

        
    def _make_train_val_dir(self):
        
        
        for yolo_path in (os.path.join(self.output_dir, 'train', 'labels/'), 
                          os.path.join(self.output_dir, 'val', 'labels/'),
                          os.path.join(self.output_dir, 'train', 'images/'), 
                          os.path.join(self.output_dir, 'val', 'images/')):
            if os.path.exists(yolo_path):
                shutil.rmtree(yolo_path)
            
            os.makedirs(yolo_path)    
                
    def _get_label_id_map(self, json_dir):
        
        if self.classes_file is not None:
            df = pd.read_csv(self.classes_file,header=None)
            df.columns=["names"]
            df["id"] = df.index
            
            unordered_dict = df.set_index('names').T.to_dict('records')[0]
            
             # Then order it
            dict_to_return = OrderedDict((k,unordered_dict.get(k)) for k in df.names)
        
        else:
            
        
            label_set = set()
        
            for file_name in os.listdir(json_dir):
                if file_name.endswith('json'):
                    json_path = os.path.join(json_dir, file_name)
                    data = json.load(open(json_path))
                    for shape in data['shapes']:
                        label_set.add(shape['label'])
                        
            dict_to_return = OrderedDict([(label, label_id) for label_id, label in enumerate(label_set)])
        
        return dict_to_return
    
    def _train_test_split(self, folders, json_names, val_size):
        if len(folders) > 0 and 'train' in folders and 'val' in folders:
            train_folder = os.path.join(self._json_dir, 'train/')
            train_json_names = [train_sample_name + '.json' \
                                for train_sample_name in os.listdir(train_folder) \
                                if os.path.isdir(os.path.join(train_folder, train_sample_name))]
            
            val_folder = os.path.join(self._json_dir, 'val/')
            val_json_names = [val_sample_name + '.json' \
                              for val_sample_name in os.listdir(val_folder) \
                              if os.path.isdir(os.path.join(val_folder, val_sample_name))]
            
            return train_json_names, val_json_names
        
        if val_size != 0:
            train_idxs, val_idxs = train_test_split(range(len(json_names)), 
                                                    test_size=val_size)
            train_json_names = [json_names[train_idx] for train_idx in train_idxs]
            val_json_names = [json_names[val_idx] for val_idx in val_idxs]
        else:
            train_json_names = json_names
            val_json_names = []
        
        return train_json_names, val_json_names
    
    def convert(self, val_size):
        """
        json_names = [file_name for file_name in os.listdir(self._json_dir) \
                      if os.path.isfile(os.path.join(self._json_dir, file_name)) and \
                      file_name.endswith('.json')]
        """
        
        self.list_images = list(paths.list_images(self._json_dir))
        #json_names = [os.path.splitext(s)[0]+".json" for s in self.list_images]
        json_names = [os.path.splitext(os.path.split(s)[1])[0]+".json" for s in self.list_images]

        
        
        folders =  [file_name for file_name in os.listdir(self._json_dir) \
                    if os.path.isdir(os.path.join(self._json_dir, file_name))]
        train_json_names, val_json_names = self._train_test_split(folders, json_names, val_size)
        
        self._make_train_val_dir()
        
        # convert labelme object to yolo format object, and save them to files
        # also get image from labelme json file and save them under images folder
        
        print("Working on train dataset...")
        Parallel(n_jobs=self.number_cores)(delayed(self.convert_one)(target_dir,json_name) for target_dir, json_name in tqdm(zip(['train/']*len(train_json_names), train_json_names), total=len(train_json_names)))
        
        print("Working on val dataset...")
        Parallel(n_jobs=self.number_cores)(delayed(self.convert_one)(target_dir,json_name) for target_dir, json_name in tqdm(zip(['val/']*len(val_json_names), val_json_names), total=len(val_json_names)))

        print('Generating data.yaml file ...')
        self._save_dataset_yaml()
                
    def convert_one(self, target_dir, json_name):
        
        json_path = os.path.join(self._json_dir, json_name)
        json_data = json.load(open(json_path))


        img_path = self._save_yolo_image(json_data, 
                                         json_name, 
                                         os.path.join(self.output_dir,target_dir,'images'), 
                                         target_dir)
            
        yolo_obj_list = self._get_yolo_object_list(json_data, img_path)
        self._save_yolo_label(json_name, 
                              target_dir, 
                              yolo_obj_list)
        
        
    
    def _get_yolo_object_list(self, json_data, img_path):
        yolo_obj_list = []
        
        img_h, img_w, _ = cv2.imread(img_path).shape
        for shape in json_data['shapes']:
            # labelme circle shape is different from others
            # it only has 2 points, 1st is circle center, 2nd is drag end point
            if shape['shape_type'] == 'circle':
                yolo_obj = self._get_circle_shape_yolo_object(shape, img_h, img_w)
            else:
                yolo_obj = self._get_other_shape_yolo_object(shape, img_h, img_w)
            
            yolo_obj_list.append(yolo_obj)
            
        return yolo_obj_list
    
    def _get_circle_shape_yolo_object(self, shape, img_h, img_w):
        obj_center_x, obj_center_y = shape['points'][0]
        
        radius = math.sqrt((obj_center_x - shape['points'][1][0]) ** 2 + 
                           (obj_center_y - shape['points'][1][1]) ** 2)
        obj_w = 2 * radius
        obj_h = 2 * radius
        
        yolo_center_x= round(float(obj_center_x / img_w), 6)
        yolo_center_y = round(float(obj_center_y / img_h), 6)
        yolo_w = round(float(obj_w / img_w), 6)
        yolo_h = round(float(obj_h / img_h), 6)
            
        label_id = self._label_id_map[shape['label']]
        
        return label_id, yolo_center_x, yolo_center_y, yolo_w, yolo_h
    
    def _get_other_shape_yolo_object(self, shape, img_h, img_w):
        def __get_object_desc(obj_port_list):
            __get_dist = lambda int_list: max(int_list) - min(int_list)
            
            x_lists = [port[0] for port in obj_port_list]        
            y_lists = [port[1] for port in obj_port_list]
            
            return min(x_lists), __get_dist(x_lists), min(y_lists), __get_dist(y_lists)
        
        obj_x_min, obj_w, obj_y_min, obj_h = __get_object_desc(shape['points'])
                    
        yolo_center_x= round(float((obj_x_min + obj_w / 2.0) / img_w), 6)
        yolo_center_y = round(float((obj_y_min + obj_h / 2.0) / img_h), 6)
        yolo_w = round(float(obj_w / img_w), 6)
        yolo_h = round(float(obj_h / img_h), 6)
            
        label_id = self._label_id_map[shape['label']]
        
        return label_id, yolo_center_x, yolo_center_y, yolo_w, yolo_h
    
    def _save_yolo_label(self, json_name, target_dir, yolo_obj_list):
        txt_path = os.path.join(self.output_dir, target_dir, 
                                'labels', 
                                json_name.replace('.json', '.txt'))
        
        with open(txt_path, 'w+') as f:
            for yolo_obj_idx, yolo_obj in enumerate(yolo_obj_list):
                yolo_obj_line = '%s %s %s %s %s\n' % yolo_obj \
                    if yolo_obj_idx + 1 != len(yolo_obj_list) else \
                    '%s %s %s %s %s' % yolo_obj
                f.write(yolo_obj_line)
                
    def _save_yolo_image(self, json_data, json_name, image_dir_path, target_dir):
        
        img_path_in = [s for s in self.list_images if os.path.join(self._json_dir,json_name.replace('.json', '.')) in s]
        
        if not (len(img_path_in) == 1) or (len(img_path_in) == 0):
            print("Warning!!! image not found, using metadata saved in json")
            print(img_path_in)

        if not os.path.exists(img_path_in[0]):
            img_name = json_name.replace('.json', '.png')
            img_path_out = os.path.join(image_dir_path, img_name)
            img = utils.img_b64_to_arr(json_data['imageData'])
            PIL.Image.fromarray(img).save(img_path_out)
        else:
            img_path_in = img_path_in[0]
            img_path_out = os.path.join(image_dir_path,os.path.split(img_path_in)[1])
            shutil.copy(img_path_in, img_path_out)
            
        
        return img_path_out
    
    def _save_dataset_yaml(self):
        classes_df = pd.DataFrame(dict(self._label_id_map.items()).keys())
        classes_df.to_csv(os.path.join(self.output_dir, 'classes.txt'), header=None, index=None)
        
        yaml_path = os.path.join(self.output_dir, 'data.yaml')
        
        with open(yaml_path, 'w+') as yaml_file:
            yaml_file.write('train: %s\n' % \
                            os.path.join(self.output_dir, 'train/'))
            yaml_file.write('val: %s\n\n' % \
                            os.path.join(self.output_dir, 'val/'))
            yaml_file.write('nc: %i\n\n' % len(self._label_id_map))
            
            names_str = ''
            for label, _ in self._label_id_map.items():
                names_str += "'%s', " % label
            names_str = names_str.rstrip(', ')
            yaml_file.write('names: [%s]' % names_str)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_dir',type=str, help='Please input the path of the labelme json files and images.')
    parser.add_argument('--val_size',type=float, nargs='?', default=None, help='Please input the validation dataset size, for example 0.1 ')
    parser.add_argument('--output_dir', type=str, default= "output", help='The directory where images and label files will be placed')
    parser.add_argument('--number_cores', default=4, type=int, help='Whether or not to use multiple cores (default=4)')
    parser.add_argument('--classes_file', default=None, type=str, help='Provide classes.txt file for specific order')
    args = parser.parse_args(sys.argv[1:])
    
    #number_cores = args.number_cores
    
    # set_objejt     
    convertor = Labelme2YOLO(args.json_dir, args.number_cores, args.output_dir, args.classes_file)
    
    # Run convert
    convertor.convert(val_size=args.val_size)
