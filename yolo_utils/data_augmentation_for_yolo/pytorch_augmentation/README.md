# Data augmentation for bounding boxes

## Geometric

### Quick Start

The structure to run the script is:

`python geometric_bboxes.py -i [DATASET INPUT] -o [DATASET OUTPUT] --flags`

How to run, there are two ways:

1) Run with its options

    ```
	python geometric_bboxes.py --rotate
    python geometric_bboxes.py --translateX
    python geometric_bboxes.py --translateY
    python geometric_bboxes.py --shearX
    python geometric_bboxes.py --shearY
    python geometric_bboxes.py --flip
    python geometric_bboxes.py --full
	```
    
	Add the flags you need, example:
	
    `python geometric_bboxes.py -i [DATASET INPUT] -o [DATASET OUTPUT] --rotate --
	translateX --translateY --shearX --shearY`
	
    `python geometric_bboxes.py -i [DATASET INPUT] -o [DATASET OUTPUT] --rotate --flip`
    
2) Run all data augmentations

    `python geometric_bboxes.py -i [DATASET INPUT] -o [DATASET OUTPUT] --full`

### Data Augmentation

* Original photo

<img src="assets/orginal photo.png">

* Rotate

<img src="assets/geometric_rotate.png">

* TranslateX

<img src="assets/geometric_translateX.png">

* TranslateY

<img src="assets/geometric_translateY.png">

* ShearX

<img src="assets/geometric_shearX.png">

* ShearY

<img src="assets/geometric_shearY.png">

* Flip

<img src="assets/geometric_flip.png">




## Color

### Quick Start

The structure to run the script is:

`python color_bboxes.py -i [DATASET INPUT] -o [DATASET OUTPUT] --flags`

How to run, there are two ways:

1) Run with its options

    ```
	python color_bboxes.py --cutout
    python color_bboxes.py --solarize
    python color_bboxes.py --equalize
	```
    
	Add the flags you need, example:
	
    `python color_bboxes.py -i [DATASET INPUT] -o [DATASET OUTPUT] --solarize --equalize`
    
2) Run all data augmentations

    `python color_bboxes.py -i [DATASET INPUT] -o [DATASET OUTPUT] --full`

### Data Augmentation

* Original photo

<img src="assets/orginal photo.png">

* Cutout

<img src="assets/color_cutout.png">

* Solarize

<img src="assets/color_solarize.png">

* Equalize

<img src="assets/color_equalize.png">


