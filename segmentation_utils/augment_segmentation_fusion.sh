rm -r yolo/datasets/fusion/classes.txt yolo/datasets/fusion/data.yaml yolo/datasets/fusion/train yolo/datasets/fusion/val yolo/datasets/fusion/train_orig/annotations.json yolo/datasets/fusion/val_orig/annotations.json
train_labelme=~/Projects/yolo/datasets/fusion/train_orig/
val_labelme=~/Projects/yolo/datasets/fusion/val_orig/
augment_val= false # false is recommended

# ===================== Convert to coco_json: outputs will be saved into the same folder 'annotations.json' ========================== #
echo Converting labelme to coco format...
cd python_utils/segmentation_utils/labelme2coco/

# Convert train set
python labelme2coco.py --input $train_labelme

# Convert validation set
python labelme2coco.py --input $val_labelme


# ==============  Data augmentation for coco: the output will still be in coco format ========================== #
echo Applying augmentations to coco format...
cd ../data_augmentation/

# Augmentation for train
train_augmentation="$(dirname "$train_labelme")"/train_aug/ # This is the output of images augmented, the directory will labelme path + 'val_aug'
python data_aug.py -i $train_labelme -o $train_augmentation --test --rotate --translateX --translateY --shear --gamma --equalize --dropout --gaussian --copy-orig --elastic # No horizontal flip (--flip)
#python data_aug.py -i $train_labelme -o $train_augmentation --full #Run all data augmentations



# Augmentation for val: it will be applied just in case augment_val flag is set to true (not recommended)
val_augmentation="$(dirname "$val_labelme")"/val_aug/ # This is the output of images augmented, the directory will labelme path + 'val_aug'
if $augment_val; then
	# python data_aug.py -i $val_labelme -o $val_augmentation --rotate --translateX --translateY --shear --gamma --equalize --dropout --gaussian --copy_orig # No horizontal flip (--flip)
	python data_aug.py -i $val_labelme -o $val_augmentation --copy-orig #Run all data augmentations
else
	python data_aug.py -i $val_labelme -o $val_augmentation --copy-orig # Just copy images
fi


# =============== Convert to yolo format: ============================= #
echo Converting coco to yolo segmentation format...
cd ../json2yolo/


# Convert train set
python general_json2yolo.py --input $train_augmentation --use-segments --output "$(dirname "$train_labelme")"/train/ # Import to add the flag --use-segments otherwise they will be converted into bounding boxes
#rm -r $train_augmentation

# Convert validation set. Highly recommendable 'classes.txt' file set equal to output train
python general_json2yolo.py --input $val_augmentation --use-segments --output "$(dirname "$val_labelme")"/val/ --classes-file "$(dirname "$val_labelme")"/classes.txt # Import to add the flag --use-segments otherwise they will be converted into bounding boxes
#rm -r $val_augmentation
