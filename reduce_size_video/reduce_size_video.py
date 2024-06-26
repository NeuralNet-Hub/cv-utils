

%reset -f
import cv2
from imutils import paths
import os
import numpy as np
import time


args={"input":"data_in",
      "output":"data_out",
      "height":640,
      "width":480}


list_files=list(paths.list_files(args["input"]))
h=args["height"]
w=args["width"]

j=1
for file in list_files:
    
    print(str(j)+" from "+str(len(list_files)))
    print("Reducing size of frame from file "+file)
    file_name=file.split(os.path.sep)
    file_name=file_name[len(file_name)-1]
    file_name=file_name.split(".mp4")[0]

    vs = cv2.VideoCapture(file)
    fps_video_original=vs.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = None
    time.sleep(2.0)

    while True:
       	# read the next frame from the file
       	(grabbed, frame) = vs.read()
    
       	# if the frame was not grabbed, then we have reached the end
       	# of the stream
       	if not grabbed:
       		break
        
        frame=cv2.resize(frame,(h,w))
        
        """
        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        """
        
        
        if args["output"] != "" and writer is None:
            # initialize our video writer
            #fourcc = cv2.VideoWriter_fourcc(*"H264")
            #fourcc = cv2.cv.CV_FOURCC(*'H264')
            writer = cv2.VideoWriter(args["output"]+os.path.sep+file_name+".avi", fourcc, int(fps_video_original),(frame.shape[1], frame.shape[0]), True)
        
        if writer is not None:
            writer.write(frame)
        
    j+=1