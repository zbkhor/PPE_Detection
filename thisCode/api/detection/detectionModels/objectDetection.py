# Author: Tharine Ramachandran
# Data Written: 10/08/2020
#!/usr/bin/env python
import numpy as np
from numpy import pi, sin, cos , asarray
import matplotlib.pyplot as plt 
import cv2 as cv 
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
from SafetyManagerApp.models import detectionObject
from SafetyManagerApp.settings import DETECTION_MODELS_DIR as url

# this method takes and image and checks if a hard hat is present in the image 
def helmetDetectionModel (detectionImage):

    # Get current working directory
    cwd = os.getcwd()
    newCwd = cwd.replace(os.sep, '/')

     # URL to the   model
    pb  = os.path.join(url,  'HardHatModel' ,'Hardhat_frozen_inference_graph.pb')          
    pbtxt  = os.path.join(url,  'HardHatModel' ,'Hardhat_graph.pbtxt')          
    
    # Load a model imported from Tensorflow
    tensorflowNet = cv2.dnn.readNetFromTensorflow(pb,pbtxt) 

      # Input image
    img =  cv.cvtColor(detectionImage, cv.COLOR_BGR2RGB) 
    rows, cols, channels = img.shape
 
    # Use the given image as input, which needs to be blob(s).
    tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
 
    # Runs a forward pass to compute the net output
    networkOutput = tensorflowNet.forward()
 
    # Create variable for isHardhat
    isHardhat = False
    values = []
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
                values =  [int(left), int(top), int(right), int(bottom)]  
                isHardhat=True
                break
    except Exception as ex:
        print (ex)
        
    # returns detection results
    helmentDetection =   detectionObject()
    helmentDetection.detection = isHardhat
    helmentDetection.coordinates = values
    helmentDetection.partDetection = isHardhat  
    helmentDetection.equipment =14

    return  helmentDetection
    
# this method takes and image and checks if a hard hat is present in the image 
def gloveDetectionModel (detectionImage):
    # Get current working directory
    cwd = os.getcwd()
    newCwd = cwd.replace(os.sep, '/')
 
    # load URL
    pb  = os.path.join(url,  'GlovesModel' ,'gloves_frozen_inference_graph.pb')          
    pbtxt  = os.path.join(url,  'GlovesModel' ,'gloves_graph.pbtxt')          
        
    # Load a model imported from Tensorflow
    tensorflowNet = cv2.dnn.readNetFromTensorflow(pb,pbtxt)
         
    # Input image
    img = detectionImage
    rows, cols, channels = img.shape
 

 
    # Create variable for isHardhat
    isGlove = False
    results = []
    glovesDetected = detectionObject()
    glovesDetected.coordinates = []
    glovesDetected.detection = False 
    glovesDetected.partDetection = False 
    glovesDetected.equipment = 13
    try:
         
        # Use the given image as input, which needs to be blob(s).
        tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))
 
        # Runs a forward pass to compute the net output
        networkOutput = tensorflowNet.forward()
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
                values = [int(left), int(top), int(right), int(bottom)]
                glovesDetected.partDetection = True 
                results.append(values)
    # error flow
    except Exception as ex:
        print (ex)
    # if no glove is detected 
    if len(results) == 2 :
        glovesDetected.coordinates = results
        glovesDetected.detection = True 
        
          
    return   glovesDetected
 

# this method takes an image then detects the person in the image then checks if the object is present 
def personcheck (detectionImage): 

    # url to model 
    pb  =      os.path.join(url,  'PersonModel' ,'Person_frozen_inference_graph.pb')          
    pbt =   os.path.join(url,'PersonModel' ,'Person_ssd_mobilenet_v1_coco.pbtxt')   

    #url to image
    image = cv.cvtColor(detectionImage, cv.COLOR_BGR2RGB)    

    #class detected in the model
    classes = { 1: 'person'}
 
    #load the model
    cvNet = cv.dnn.readNetFromTensorflow(pb,pbt)   
     
    rows = image.shape[0]
    cols = image.shape[1] 
    
    # detection of the image
    cvNet.setInput(cv.dnn.blobFromImage(image, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
 
    #initialize values 
    cvOut = cvNet.forward()
    persons = [] 
    count = 0
    personCoordinates = []
    try :
        for detection in cvOut[0,0,:,:]:
            score = float(detection[2])
            
            # if confidence of the detection is more than 50 percent
            if score > 0.7:
                
                class_id = int(detection[1])
                
                # if the person class is detected 
                if class_id == 1 :

                    # get coordinates of the person in the image 
                    left = detection[3] * cols
                    top = detection[4] * rows
                    right = detection[5] * cols
                    bottom = detection[6] * rows   

                    # store the coordinates of the person 
                    person = ( int(left)  , int(top)   , int(right)  , int(bottom)    )  
                    personCoordinates.append(person)

    except Exception as ex :
        print (ex)
    return personCoordinates


# this method takes an image then detects the person in the image then checks if the object is present 
def detection (domain,checkForObjects ,itemDetectionList ,detectionImage ): 
     
    personCoordinates = personcheck(detectionImage)
    count = len(personCoordinates)
    if checkForObjects :
        # if   one person is detected 
        if count == 1 :
        
            try :
             # init values
                listPersonDetection=[]
                equipmentDetection = {}
                detectionImageequipmentsDetected = []
                   
                for equipment in itemDetectionList :

                    # check for hard hat
                    if equipment == 14 :
                        listPersonDetection.append(helmetDetectionModel(detectionImage) )

                    # check for gloves
                    if equipment == 13 :
                        listPersonDetection.append(gloveDetectionModel (detectionImage))
                                             
                # return results
                log = {  "detections" : listPersonDetection   , "humanDetections" : True } 
             # error flow
            except Exception as ex :
                # return error
                log = {   'errorMessage' : 'An error occurred',  "humanDetections" : False  } 
 
            # return results
            return   log  
        # if no person is detected
        elif count == 0 :
            # if no person is detected 
            payload =  { 'errorMessage' : 'no person was detected',"humanDetections" : False  } 

        else : 
            # if too many person is detected
            payload ={ 'errorMessage' :'too many persons detected from the image',"humanDetections" : False  } 
    else : 
        # if no object check
        if count > 0 :
            error = 'a person was detected'
            humanDetections = True
        else :
            error = 'no person was detected'
            humanDetections = False
        payload ={ 'errorMessage' :error ,"humanDetections" : humanDetections  }  
    
    return payload
     
 