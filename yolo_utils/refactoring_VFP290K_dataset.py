import os
import xmltodict
import munch
import argparse
from tqdm import tqdm
import numpy as np
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="dataset_input",
                    help="input folder",
                    default="data_in")
parser.add_argument("-o",
                    dest="dataset_output",
                    help="directory to store generated data. this directory will be made automatically.",
                    default="data_out")
parser.add_argument("-prob",
                    dest="prob",
                    help="probability to get the image",
                    type = float,
                    default = 0.05)
args = parser.parse_args()
dataset_input = args.dataset_input
dataset_output = args.dataset_output
prob = args.prob


dirname_output_image = os.path.join( dataset_output , "images" )
dirname_output_label = os.path.join( dataset_output , "labels" )

# ============================== Aux functions =================================== #

def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def xml_to_string(xml_path):
    file = open(xml_path)
    doc = xmltodict.parse(file.read())
    doc = munch.munchify(doc)

    try:
        annot = doc.annotation.object
    except:
        return ""

    if isinstance(annot, munch.Munch):
        annot = [annot]

    if len(annot) == 0:
        pass

    ret_string = ''
    for anot in annot:
        coord = anot.bndbox
        label = anot.name
        try:
            label = int(label)
            if label not in [0, 1, 2]:
                print('error occurred in', xml_path)
                print(label, coord)
                label = input("revised label: ")
        except:
            print('error occurred in', xml_path)
            print(label, coord)
            label = input("revised label: ")
        if int(label) == 2:
            continue
        center_x = ((float(coord.xmax) + float(coord.xmin)) / 2) / 1920.0
        center_y = ((float(coord.ymax) + float(coord.ymin)) / 2) / 1080.0
        width = (float(coord.xmax) - float(coord.xmin)) / 1920.0
        height = (float(coord.ymax) - float(coord.ymin)) / 1080.0
        ret_string += '{} {} {} {} {}\n'.format(label, center_x, center_y, width, height)

    return ret_string


# ============================== End: Aux functions =================================== #


mkdir_p(dataset_output)
mkdir_p(dirname_output_image)
mkdir_p(dirname_output_label)


folders = os.listdir(dataset_input)

cont_files = 0

for path in tqdm(folders):
    path_input = os.path.join(dataset_input, path)
    dirname_input_image  = os.path.join( path_input  , "images" )
    dirname_input_label  = os.path.join( path_input  , "clean_xml" )
    image_paths = os.listdir(dirname_input_image)

    for image_name0 in image_paths:
        
        cont_files += 1
        
        if np.random.uniform(0,1) > (1-prob):
            orig_image_name = os.path.join(dirname_input_image, image_name0)
            new_image_name = os.path.join( dirname_output_image , os.path.splitext(os.path.basename(image_name0))[0]+".jpg" )
            orig_label_name = os.path.join( dirname_input_label , os.path.splitext(os.path.basename(image_name0))[0]+".xml" )
            
            # Assert both files are the same
            assert orig_label_name.split("/")[-1].split(".")[0] == orig_label_name.split("/")[-1].split(".")[0]
            
            
            # Copy image
            shutil.copy(orig_image_name,new_image_name)
            
            # Process label
            ret_string = xml_to_string(orig_label_name)
            f = open(os.path.join(dirname_output_label, os.path.basename(orig_label_name).split("/")[-1].split(".")[0]+".txt"), 'w')
            f.write(ret_string)
            f.close()

print("Total of files processed:")
print(cont_files)
