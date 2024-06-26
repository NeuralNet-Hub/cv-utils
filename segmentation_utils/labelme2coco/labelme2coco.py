import os
import argparse
import json

from labelme import utils
import numpy as np
import glob
import PIL.Image
from tqdm import tqdm
import cv2
from imutils import paths


class labelme2coco(object):
    def __init__(self, labelme_json=[], save_json_path="./coco.json", info= "", licenses = ""):
        """
        :param labelme_json: the list of all labelme json file paths
        :param save_json_path: the path to save new json
        """
        self.labelme_json = labelme_json
        self.save_json_path = save_json_path
        self.info = info
        self.licenses = licenses
        self.images = []
        self.categories = []
        self.annotations = []
        self.label = []
        self.annID = 1
        self.height = 0
        self.width = 0

        self.save_json()

    def data_transfer(self):
        for num, json_file in enumerate(tqdm(self.labelme_json)):

            with open(json_file, "r") as fp:
                data = json.load(fp)
                self.images.append(self.image(data, num, json_file))
                for shapes in data["shapes"]:
                    label = shapes["label"]#.split("_")
                    if label not in self.label:
                        self.label.append(label)
                    points = shapes["points"]
                    self.annotations.append(self.annotation(points, label, num))
                    self.annID += 1

        # Sort all text labels so they are in the same order across data splits.
        self.label.sort()
        for label in self.label:
            self.categories.append(self.category(label))
        for annotation in self.annotations:
            annotation["category_id"] = self.getcatid(annotation["category_id"])

    def image(self, data, num, json_file):
        image = {}
        try:
            img = utils.img_b64_to_arr(data["imageData"])
        except Exception as e:
            #print(e)
            with open(os.path.join("error_and_warnings.txt"), "a") as myfile:
                myfile.write("\n"+json_file)
            img_list = np.array(list(paths.list_images(os.path.split(json_file)[0])))
            img_file = img_list[np.char.startswith(img_list, os.path.splitext(json_file)[0]+".")][0]
            img = cv2.imread(img_file)

            
        height, width = img.shape[:2]
        img = None
        image["height"] = height
        image["width"] = width
        image["id"] = num
        image["file_name"] = data["imagePath"].split("/")[-1]

        self.height = height
        self.width = width

        return image

    def category(self, label):
        category = {}
        category["supercategory"] = label
        category["id"] = len(self.categories)
        category["name"] = label
        return category

    def annotation(self, points, label, num):
        annotation = {}
        contour = np.array(points)
        x = contour[:, 0]
        y = contour[:, 1]
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        annotation["segmentation"] = [list(np.asarray(points).flatten())]
        annotation["iscrowd"] = 0
        annotation["area"] = area
        annotation["image_id"] = num

        annotation["bbox"] = list(map(float, self.getbbox(points)))

        annotation["category_id"] = label  # self.getcatid(label)
        annotation["id"] = self.annID
        return annotation

    def getcatid(self, label):
        for category in self.categories:
            if label == category["name"]:
                return category["id"]
        print("label: {} not in categories: {}.".format(label, self.categories))
        exit()
        return -1

    def getbbox(self, points):
        polygons = points
        mask = self.polygons_to_mask([self.height, self.width], polygons)
        return self.mask2box(mask)

    def mask2box(self, mask):

        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]

        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        return [
            left_top_c,
            left_top_r,
            right_bottom_c - left_top_c,
            right_bottom_r - left_top_r,
        ]

    def polygons_to_mask(self, img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco = {}
        data_coco["info"] = self.info
        data_coco["licenses"] = self.licenses
        data_coco["images"] = self.images
        data_coco["categories"] = self.categories
        data_coco["annotations"] = self.annotations
        return data_coco

    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()

        os.makedirs(
            os.path.dirname(os.path.abspath(self.save_json_path)), exist_ok=True
        )
        json.dump(self.data_coco, open(self.save_json_path, "w"), indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="labelme annotation to coco data json file.")
    parser.add_argument("--input", help="Directory to labelme images and annotation json files.", type=str, default="images")
    parser.add_argument("--output", help="Directory to save annotations.json. The output will always be your_path/annotations.json", default = None)
    parser.add_argument("--info", help="If you want to add some info for the dataset", default="")
    parser.add_argument("--licenses", help="If you want to add some licenses for the dataset", default="")
    args = parser.parse_args()
    
    input, output, info, licenses = args.input, args.output, args.info, args.licenses
    
    # ==== Strat: create output folder to save annotations ==== #
    
    if output is None:
        output = os.path.join(input) #,'coco_annotations')
        
    else:
        output = os.path.join(output) #,'coco_annotations')

    if not os.path.exists(output):
        os.mkdir(output)

    output = os.path.join(output, 'annotations.json')        

    if os.path.exists(output):
        os.remove(output)
    
    # ==== End: create output folder to save annotations ==== #
        
    # Run conversion
    labelme_json = glob.glob(os.path.join(input, "*.json"))
    labelme2coco(labelme_json, output, info, licenses)
