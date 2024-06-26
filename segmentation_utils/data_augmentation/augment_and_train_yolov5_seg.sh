#!/bin/bash




# ===================== Setting global values (Please modify) ========================== #

# Set workspace and output of the augmentetd dataset Some examples as follow they should be set you once.
workspace=/home/henry/Projects/python_utils/

# datasset paths
dataset_path=/home/henry/Projects/synthetic-data-generator/output_ladder/
train_labelme=$dataset_path/train_orig
val_labelme=$dataset_path/val_orig/
augment_val= false # false is recommended



# ===================== Activate a screen using 'screen -S augmentation_train' ========================== #

# virtualenv activation
virtualenv_path=`which virtualenvwrapper.sh`
source $virtualenv_path

workon general




# ===================== Convert to coco_json: outputs will be saved into the same folder 'annotations.json' ========================== #
echo Converting labelme to coco format...
cd $workspace/segmentation_utils/labelme2coco/

# Convert train set
python labelme2coco.py --input $train_labelme

# Convert validation set
python labelme2coco.py --input $val_labelme


# ==============  Data augmentation for coco: the output will still be in coco format ========================== #
echo Applying augmentations to coco format...
cd $workspace/segmentation_utils/data_augmentation/

# Augmentation for train
train_augmentation="$(dirname "$train_labelme")"/train_aug/ # This is the output of images augmented, the directory will labelme path + 'val_aug'
#python data_aug.py -i $train_labelme -o $train_augmentation --average-blurring --rotate --translateX --translateY --shear --gamma --equalize --dropout --gaussian --copy-orig # No horizontal flip (--flip) Elastic is broken the training process
python data_aug.py -i $train_labelme -o $train_augmentation --copy-orig #Run all data augmentations



# Augmentation for val: it will be applied just in case augment_val flag is set to true (not recommended)
val_augmentation="$(dirname "$val_labelme")"/val_aug/ # This is the output of images augmented, the directory will labelme path + 'val_aug'
if $augment_val; then
	#python data_aug.py -i $val_labelme -o $val_augmentation --average-blurring --rotate --translateX --translateY --shear --gamma --equalize --dropout --gaussian --copy-orig # No horizontal flip (--flip)
	python data_aug.py -i $val_labelme -o $val_augmentation --copy-orig #Run all data augmentations
else
	python data_aug.py -i $val_labelme -o $val_augmentation --copy-orig # Just copy images
fi


# =============== Convert to yolo format: ============================= #
echo Converting coco to yolo segmentation format...
cd $workspace/segmentation_utils/json2yolo/


# Convert train set
python general_json2yolo.py --input $train_augmentation --use-segments --output "$(dirname "$train_labelme")"/train/ # Import to add the flag --use-segments otherwise they will be converted into bounding boxes
#rm -r $train_augmentation

# Convert validation set. Highly recommendable 'classes.txt' file set equal to output train
python general_json2yolo.py --input $val_augmentation --use-segments --output "$(dirname "$val_labelme")"/val/ --classes-file "$(dirname "$val_labelme")"/classes.txt # Import to add the flag --use-segments otherwise they will be converted into bounding boxes
#rm -r $val_augmentation





# ============================================================================================== #
# __   __   ___    _        ___            ____  
# \ \ / /  / _ \  | |      / _ \  __   __ | ___| 
#  \ V /  | | | | | |     | | | | \ \ / / |___ \ 
#   | |   | |_| | | |___  | |_| |  \ V /   ___) |
#   |_|    \___/  |_____|  \___/    \_/   |____/ 
# ============================================================================================== #                          



#screen -S yolov5
workon yolov5

# change to yolov5 path
yolov5_path=/home/henry/Projects/yolo/yolov5/
cd $yolov5_path
git pull

# config parameters yolov5
weights='yolov5x-seg.pt'
data=$dataset_path/data.yaml # dataset_path has been defined above (at the beginning)
wandb_project='ladder' # wandb will save with this name, same as local
name_project='XLargeV1'
bs=160 # batch size for 4 TeslaV100 32GB
epochs=300 # put 100 in case of retrain
patience=20 # put 20 in case of retrain
cache=ram # ram in case augmented dataset is less than 100K images otherwise put disk
workers=16 # still don't know how to put all cores automatically



# Local train or 1 GPU
python segment/train.py --weights $weights --data $data --epochs $epochs --batch-size -1 --workers $workers --project $wandb_project --name $name_project --cache $cache --patience $patience --exist-ok

# python -m torch.distributed.launch --nproc_per_node 4 train.py --weights $weights --data $data --epochs $epochs --batch-size $bs --workers $workers --project $wandb_project --name $name_project --cache $cache --patience $patience --exist-ok




	
