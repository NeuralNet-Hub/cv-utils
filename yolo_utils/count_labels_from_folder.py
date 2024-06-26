import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    dest="path",
                    help="folder with labels",
                    default="data_in")
#args = parser.parse_args()
#                    help="label input folder",
#                    default="data_in")
args = parser.parse_args()

path = args.path


list_files = []

for root, dirs, files in os.walk(path):
	for file in files:
		if(file.endswith(".txt")):
			list_files.append(os.path.join(root,file))
            
            

for idx, file in enumerate(list_files):
    if not 'my_labels' in locals():
        try:
            my_labels = pd.read_csv(file,header=None, sep = " ")
        except Exception as e:
            print(e)
            pass
    else:
        try:
            my_labels = my_labels.append(pd.read_csv(file,header=None, sep = " "))
        except Exception as e:
            print(str(e)+". FILE:")
            print(file)
            pass


print("============================================")
print("YOU HAVE "+str(len(list_files)) + " FILES")
print("AND "+ str(my_labels.shape[0]) + " LABELS")
print("============================================")
