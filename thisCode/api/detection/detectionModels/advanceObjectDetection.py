# Author: Tharine Ramachandran
# Data Written: 10/08/2020
#!/usr/bin/env python
from chardet import detect
import numpy as np
from numpy import pi, sin, cos , asarray
import matplotlib.pyplot as plt 
import cv2 as cv 
from SafetyManagerApp.models import detectionObject
from PIL import Image 
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np 
import cv2
import os
from PIL import Image
from numpy import asarray
import imutils
import requests 
from SafetyManagerApp.settings import DETECTION_MODELS_DIR as url
 
# this method returns the person's coordinates in the image
def personCoordinates(detectionImage) :

    # URL to the persons model
    pb  =   os.path.join(url, 'PersonModel', 'Person_frozen_inference_graph.pb')          
    pbt =   os.path.join(url, 'PersonModel', 'Person_ssd_mobilenet_v1_coco.pbtxt')     

    #read image
    image = cv.cvtColor(detectionImage, cv.COLOR_BGR2RGB)    

    # classes detected
    classes = { 1: 'person'}
     # read the network
    cvNet = cv.dnn.readNetFromTensorflow(pb,pbt)  
    
     # init values
    rows = image.shape[0]
    cols = image.shape[1] 
    cvNet.setInput(cv.dnn.blobFromImage(image, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False)) 
    cvOut = cvNet.forward() 
    count = 0
    personCoordinates = []
 
    try :
        for detection in cvOut[0,0,:,:]:
            score = float(detection[2])
            # if detected person confidence is more than 50 percent
            if score > 0.5:
                class_id = int(detection[1])

                if class_id == 1 :
                    # get coordinates
                    left = detection[3] * cols
                    top = detection[4] * rows
                    right = detection[5] * cols
                    bottom = detection[6] * rows   
                    # add person coordinates
                    # person = (( int(left) - 60, int(top)- 60, int(right)  + 60 , int(bottom) + 60))  
                    
                    # Lina edit
                    person = (( int(left), int(top), int(right), int(bottom)))
                    # end of Lina edit
                    
                    personCoordinates.append(person)

#         # Lina added
#         for i in np.arange(0, cvOut.shape[2]):
# #        for detection in cvOut[0,0,:,:]:
#             score = cvOut[0,0, i, 2]
# #            score = float(detection[2])
#             # if detected person confidence is more than 50 percent
#             if score > 0.5:
#                 class_id = int(cvOut[0,0,i,1])
#                 box = cvOut[0,0,i,3:7]* np.array([rows,cols,rows,cols])
#                 (startX, startY, endX, endY) = box.astype("int")
# #                class_id = int(detection[1])

#                 # if class_id == 1 :
#                 #     # get coordinates
#                 #     left = detection[3] * cols
#                 #     top = detection[4] * rows
#                 #     right = detection[5] * cols
#                 #     bottom = detection[6] * rows   
#                 #     # add person coordinates
#                 #     person = (( int(left) - 60, int(top)- 60, int(right)  + 60 , int(bottom) + 60))  
#                 personCoordinates.append(box)
# #                print("this is length: " + str(len(personCoordinates)))
# #                print(personCoordinates)
# #                print(personCoordinates)

#                     #draw_bounding_box(frame, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
#                 # label = str(classes[class_id])
#                 # color = COLORS[class_id]
#                 # cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
#                 # y = startY - 15 if startY - 15 > 15 else startY + 15
#                 # cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#         # end of Lina added


     # error flow                     
    except Exception as ex :
        print(ex)   
    # return values
    return personCoordinates



# this method checks for the body part coordinates using   model
def checkbody ( detectionImage, personcoords) :
    # initailze the objects checked for in this detection 
    BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

    POSE_PAIRS = [ ["Nose", "Neck"], ["LShoulder", "RShoulder"], ["LElbow", "RElbow"],
               ["LWrist", "RWrist"], ["RHip", "LHip"], ["LAnkle", "RAnkle"] ,["LEye", "LEar"] , ["REye", "LEye"],
                ["LKnee", "RKnee"]               ]

    # URL to the   model
    pb  =      os.path.join(url, 'HumanBodyPartsModel', 'humanbodyparts_graph_opt.pb')          
 
    # image checked
    croppedImg = detectionImage[personcoords[1]:personcoords[3], personcoords[0]:personcoords[2]]
    imgFrame = cv.cvtColor(croppedImg, cv.COLOR_BGR2RGB)     
    frame = asarray(imgFrame)
    #initailze variables 
    pointset = []
    inWidth = 368
    inHeight = 368 
    thr = 0.2
    net = cv.dnn.readNetFromTensorflow(pb )
     
    if  thr > 0: 
        # detection of the image
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        points = []
        pointset = []
         # load image to model
        net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]  

        assert(len(BODY_PARTS) == out.shape[1])
     
        for i in range(len(BODY_PARTS)):

             # Slice heatmap of corresponging body's part.
            heatMap = out[0, i, :, :]

            # Originally, we try to find all the local maximums. To simplify a sample
            # we just find a global one. However only a single pose at the same time
            # could be detected this way.
            _, conf, _, point = cv.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]

        # Add a point if it's confidence is higher than threshold.
            points.append((int(x), int(y)) if conf > thr else None)

        # get the values of each part detected and initialize to the pairs    
        for pair in POSE_PAIRS:
            partFrom = pair[0]
            partTo = pair[1]
            assert(partFrom in BODY_PARTS)
            assert(partTo in BODY_PARTS)

            idFrom = BODY_PARTS[partFrom]
            idTo = BODY_PARTS[partTo]
              
            if points[idFrom] and points[idTo]:
                
                pointsArray = [partFrom,partTo,points[idFrom],points[idTo]]
                pointset.append(pointsArray) 
    # returns results of the points 
    return pointset

   # this method returns the list of body parts to a dictionary
def checkCoordinates(bodyDetectionpoints) :
    bodypart ={}
    try :
        for row in bodyDetectionpoints:
            bodypart[row[0]] = row[2]
            bodypart[row[1]] = row[3] 

    except Exception as ex :
        print (ex)

    return bodypart
 
# this method checks if a hard hat is present in the image
def checkHardHat (dictBodyPart,detectionImage, eachpax):
    # init values
    array =[]
    detectionresult = detectionObject()
    detectionresult.equipment = 14
    detectionresult.detection = False
    detectionresult.coordinates = []

    # Lina added
    detectionresult.personcoords = eachpax
    detectionresult.numofpersons = 1
    # detectionresult.detection = []
    # detectionresult.partDetection = []
    # end of Lina added
    try :

        # if body part in dictionary
        
        # if shoulder in dictionary
        if 'REye' in dictBodyPart.keys()    :
            array = dictBodyPart['REye']

        elif 'LEye' in dictBodyPart.keys()    :
            array = dictBodyPart['LEye']
             
        elif 'LEar' in dictBodyPart.keys()    :
            array = dictBodyPart['LEar']

        elif 'REar' in dictBodyPart.keys()    :
           array = dictBodyPart['REar']
            
        elif 'Neck' in dictBodyPart.keys()    :
            array = dictBodyPart['Neck']
        elif 'Nose' in dictBodyPart.keys():
            array = dictBodyPart['Nose']
        else :
            detectionresult.partDetection = False 

        if array :                       
            detectionresult.partDetection = True 
            # Get current working directory
            cwd = os.getcwd()
            newCwd = cwd.replace(os.sep, '/')
 
            # URL to the   model
            pb  = os.path.join(url, 'HardHatModel', 'saved_model.pb')          
            # pbtxt  = os.path.join(url, 'HardHatModel', 'graph12-10200.pbtxt')
 
            # Load a model imported from Tensorflow
            tensorflowNet = cv2.dnn.readNetFromTensorflow(pb)
 
            # Input image
            croppedImg = detectionImage[eachpax[1]:eachpax[3], eachpax[0]:eachpax[2]]
            img =  cv.cvtColor(croppedImg, cv.COLOR_BGR2RGB)  
            rows, cols, channels = img.shape
 
            # Use the given image as input, which needs to be blob(s).
            tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
 
            # Runs a forward pass to compute the net output
            networkOutput = tensorflowNet.forward()
 
            # Create variable for isHardhat
            isHardhat = False
            results = []
            personcount = 0
            try:
                # Loop on the outputs
                for detection in networkOutput[0,0]:

                    # detection.personindex = personcount + 1 # Lina added

                    category = int(detection[1])
                    score = float(detection[2])
                    # score = networkOutput[0,0,i,2]

                    # checks if output has confidance more than 70 percent than sends the output
                    if score > 0.7:
                        left = detection[3] * cols
                        top = detection[4] * rows
                        right = detection[5] * cols
                        bottom = detection[6] * rows 
                        
                        # get coordinates of the hard head and check if they overlap with the position of head 
                        # Y and X values of the coordinates
                        if( (array[0]>= int(left)  or array[1] >= int(right) )  or (array[2]>= int(top)  or array[3] >= int(bottom))      ):
                            detectionresult.detection = True 
                            detectionresult.coordinates = [int(left), int(top), int(right), int(bottom)]
                            break

            except Exception as ex:
                print (ex)
        
    except Exception as ex: 
        print (ex)
    # return result 
    return   detectionresult
    
# this method checks if a glove is present in the image
def checkGloves (dictBodyPart,detectionImage):
    
    # init values
    detectionresult = detectionObject()
    detectionresult.equipment = 13
    detectionresult.detection = False
    detectionresult.partDetection = True
    detectionresult.coordinates = []
    detectionCoordinates = []
    values = []
    try :
        array =[]
         
        # Get current working directory
        cwd = os.getcwd()
        newCwd = cwd.replace(os.sep, '/')
 
        # URL to the   model
        pb  = os.path.join(url,  'GlovesModel' ,'gloves_frozen_inference_graph.pb')          
        pbtxt  = os.path.join(url,  'GlovesModel' ,'gloves_graph.pbtxt')          
        
        # Load a model imported from Tensorflow
        tensorflowNet = cv2.dnn.readNetFromTensorflow(pb,pbtxt)
         
        # Input image
        img =detectionImage
        rows, cols, channels = img.shape
 
        # Use the given image as input, which needs to be blob(s).
        tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
 
        # Runs a forward pass to compute the net output
        networkOutput = tensorflowNet.forward()
 
        # Create variable for isHardhat
        isHardhat = False
        results = []
        try:
            # Loop on the outputs
            for detection in networkOutput[0,0]:

                category = int(detection[1])
                score = float(detection[2])

                # checks if output has confidance more than 70 percent than sends the output
                if score > 0.7:
                    left = detection[3] * cols
                    top = detection[4] * rows
                    right = detection[5] * cols
                    bottom = detection[6] * rows 
                    # init values
                    coordinatesValues= [int(left), int(top), int(right), int(bottom)]
                    values.append(coordinatesValues)
         # error flow                    
        except Exception as ex:
            print (ex)

        ## if shoulder in dictionary
        #if 'LShoulder' in dictBodyPart.keys()    :
        #    LValues = [ dictBodyPart['LShoulder'][0],0,cols,rows]

        #if 'LEar' in dictBodyPart.keys()    :
        #    LValues = [ dictBodyPart['LEar'][0],0,cols,rows]

        ## if shoulder in dictionary
        #if 'RShoulder' in dictBodyPart.keys()  :
        #    RValues = [0,0,dictBodyPart['RShoulder'][0],rows]

        #if 'REar' in dictBodyPart.keys()    :
        #    RValues = [0,0,dictBodyPart['REar'][0],rows]
            
             

        #if None not in (values,RValues,LValues):  
        #    detectionresult.partDetection = True
        #    for coordinates in values:
        #        # check if glove values are  valid (on the arm)
        #        if (coordinates[0]<(RValues[2]  + 60)) or (coordinates[0]> (LValues[0] - 60)):
        #            detectionCoordinates.append(coordinates)
            
                # set values
        if len(values) == 2:
            detectionresult.detection = True
            
            detectionresult.coordinates = values

    #error flow
    except Exception as ex:
        print (ex)
        # return result 
    return   detectionresult
     