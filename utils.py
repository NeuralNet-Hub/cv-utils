import cv2
import numpy as np
#from tensorflow.keras.preprocessing.image import img_to_array


def detect_and_predict_age_gender(frame, faceNet, ageNet,genderNet, minConf=0.5):
	# define the list of age buckets our age detector will predict
	AGE_BUCKETS = ["(0-2)", "(4-6)", "(8-12)", "(15-20)", "(25-32)",
		"(38-43)", "(48-53)", "(60-100)"]
    
	GENDER_BUCKETS = ["male","female"]

	# initialize our results list
	results = []

	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > minConf:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# extract the ROI of the face
			face = frame[startY:endY, startX:endX]

			# ensure the face ROI is sufficiently large
			if face.shape[0] < 20 or face.shape[1] < 20:
				continue

			# construct a blob from *just* the face ROI
			faceBlob = cv2.dnn.blobFromImage(face, 1.0, (227, 227),
				(78.4263377603, 87.7689143744, 114.895847746),
				swapRB=False)

			# make predictions on the age and find the age bucket with
			# the largest corresponding probability
			ageNet.setInput(faceBlob)
			preds = ageNet.forward()
			i = preds[0].argmax()
			age = AGE_BUCKETS[i]
			ageConfidence = preds[0][i]
            
			
            # make predictions on the gender and find the gender bucket with
			# the largest corresponding probability
			genderNet.setInput(faceBlob)
			preds = genderNet.forward()
			i = preds[0].argmax()
			gender = GENDER_BUCKETS[i]
			genderConfidence = preds[0][i]
            
            
			"""
            # preprocessing for gender detection model
			face_crop = cv2.resize(face, (96,96))
			face_crop = face_crop.astype("float") / 255.0
			face_crop = img_to_array(face_crop)
			face_crop = np.expand_dims(face_crop, axis=0)

			# apply gender detection on face
			genderConfidence = genderNet.predict(face_crop)[0] # model.predict return a 2D matrix, ex: [[9.9993384e-01 7.4850512e-05]]
			# get label with max accuracy
			idx = np.argmax(genderConfidence)
			gender = GENDER_BUCKETS[idx]
            """



			# construct a dictionary consisting of both the face
			# bounding box location along with the age prediction,
			# then update our results list
			d = {
				"loc": (startX, startY, endX, endY),
				"age": (age, ageConfidence),
                "gender": (gender,genderConfidence)
			}
			results.append(d)

	# return our results to the calling function
	return results



#plot_one_box(box, frame, color=[[0,204,0]], label=text, line_thickness=3)
def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    #color = [[0,204,0]]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color[0], thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 5, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color[0], -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 5, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

    
        
def plot_one_box_two_labels(x, img, color=None, label_sup=None,label_inf=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    #color = [[0,204,0]]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color[0], thickness=tl, lineType=cv2.LINE_AA)
    
    
    if label_sup:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label_sup, 0, fontScale=tl / 5, thickness=tf)[0]
        my_c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, my_c2, color[0], -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label_sup, (c1[0], c1[1] - 2), 0, tl / 5, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    
    if label_inf:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label_inf, 0, fontScale=tl / 5, thickness=tf)[0]
        my_c1 = c2[0] - t_size[0], c2[1] +14
        my_c2 = c2[0] , c2[1] - t_size[1] + 17
        cv2.rectangle(img, my_c1, my_c2, color[0], -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label_inf, (my_c1[0], my_c1[1] - 2), 0, tl / 5, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
