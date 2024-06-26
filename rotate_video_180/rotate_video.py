
import cv2
from imutils import paths
import os
import time



args = {"input":"data_in",
        "output":"data_out"}

list_files=list(paths.list_files("data_in"))
j=1

#file=list_files[0]

for file in list_files:
    
    print(str(j)+" from "+str(len(list_files)))
    #print("Extracting frame from file "+file)
    file_name=file.split(os.path.sep)
    file_name=file_name[len(file_name)-1]
    file_name=file_name.split(".mp4")[0]

    vs = cv2.VideoCapture(file)
    
    fps_video_original=vs.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = None
    time.sleep(2.0)
    
    i=0
    while True:
        # read the next frame from the file
        (grabbed, frame) = vs.read()

        #plt.imshow(frame)

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break
    
        frame=cv2.rotate(frame, cv2.ROTATE_180) 
        
        """
        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
        	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        """"
        
        # if an output video file path has been supplied and the video
        # writer has not been initialized, do so now
        if args["output"] != "" and writer is None:
            # initialize our video writer
            #fourcc = cv2.VideoWriter_fourcc(*"H264")
            #fourcc = cv2.cv.CV_FOURCC(*'H264')
            writer = cv2.VideoWriter(args["output"]+"/"+file_name+".avi", fourcc, fps_video_original,(frame.shape[1], frame.shape[0]), True)
        
        if writer is not None:
            writer.write(frame)

    
    j+=1