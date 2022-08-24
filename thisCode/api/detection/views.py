# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SafetyManagerApp.forms  import DetectionUploadForm
from rest_framework import status
from rest_framework.response import Response 
from PIL import Image
import cv2 as cv 
from rest_framework import status
from django.http import JsonResponse,HttpResponse 
import json  
import base64  
from .serializers import DetectionsSerializer, PersonCoordSerializer
import numpy as np
import cv2
from PIL import Image 
from api.detection.detectionModels.advanceObjectDetection import personCoordinates, checkbody,checkCoordinates ,checkHardHat,checkGloves
from numpy import  asarray 
import requests  
from api.detection.detectionModels.objectDetection import detection
import os.path
from SafetyManagerApp.models import detectionObject
from SafetyManagerApp.settings import DETECTION_MODELS_DIR as url
 
def imageCropping(top,left,width,height,imagestr) :
    #init values
    imageBase64 = ''

    try :
        # get image from base64 and set image for cropping
        nparr = np.fromstring(base64.b64decode(imagestr), np.uint8) 
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        # cropping image
        crop_img = img[top:top+height, left:left+width] 
        cv.imwrite(url+'Test_timage.jpg',crop_img)
     # error flow
    except Exception as ex:
        print(ex)
    # return values
    return crop_img


#this methods gets the image and returns the objects detected in it
@csrf_exempt
def image_detection(request):
    
    # gets the form values 
    form = DetectionUploadForm(request.POST) 
    

    if form.is_valid():
        #init values
        imagestr  =  form.cleaned_data['image']   
        top = int (form.cleaned_data['top'])
        left =int (form.cleaned_data['left'])
        width =int (form.cleaned_data['width'])
        height =int (form.cleaned_data['height'])
        itemDetectionList=  form.cleaned_data['itemDetectionList']   
        itemDetectionList = list(map(int, itemDetectionList)) 
        checkForObjects = form.cleaned_data['checkForObjects']  

        # get image from base64
        detectionImage = imageCropping(top,left,width,height,imagestr)  

        # gets the base url for post 
        baseurl = request.get_host()
        # detection method is called
        body = detection( baseurl,checkForObjects ,itemDetectionList,detectionImage ) 
       # init values for return
        listtoSerializer=[]
        

        try :
            # check if detection was successful
            if 'detections' in body.keys():

                #init values
                detectionBody = body['detections']       

                # serialize list 
                serializer = DetectionsSerializer(detectionBody, many=True)

                # content for returnf
                content ={"detections": serializer.data , "humanDetections" :  body['humanDetections']   }
            else :
                # no human detected return
                content ={"detections":  body['errorMessage']    , "humanDetections" :    body['humanDetections']   }

        except :
            # error return
            content ={"errorMessage": "an error occured"  , "humanDetections" :  False }
    else :
        content ={"errorMessage":  "form is invalid" , "humanDetections" :  False   }
    # return response with data    
    json_object = json.dumps(content )   
    return  HttpResponse(json_object, content_type='text/json')


# this method uses a model to detect the human parts of the image and detects appropriate objects in those parts
@csrf_exempt
def advance_image_detection(request):
    
    # Lina added
    persondetection = detectionObject()
    persondetection.personcoords = []
    persondetection.numofpersons = 0
    # End of Lina added

    # gets data from form
    form = DetectionUploadForm(request.POST  ) 
    if form.is_valid():
        #init values
        imagestr  =  form.cleaned_data['image']  
        top = int (form.cleaned_data['top'])
        left =int (form.cleaned_data['left'])
        width =int (form.cleaned_data['width'])
        height =int (form.cleaned_data['height'])
        itemDetectionList=  form.cleaned_data['itemDetectionList']   
        itemDetectionList = list(map(int, itemDetectionList)) 
        checkForObjects = form.cleaned_data['checkForObjects']  

        #convert image to array
        detectionImage = imageCropping(top,left,width,height,imagestr)  
         
        # get base url
        baseurl = request.get_host()

        #init values
        content={}
        listtoSerializer = []
        listtoSerializer2 = []

        try :
            # check if image as a human
            # returns coordinates of person
            personcheck = personCoordinates(detectionImage)
            
            # Lina added
            persondetection.personcoords = personcheck
            persondetection.numofpersons = len(personcheck)
            listtoSerializer2.append(persondetection)
            # numofpax = len(personcheck)
            # i = 0
            # end of Lina added

            # if human detection is true
            if len(personcheck) >= 1 and checkForObjects:  # when checkForPerson(), checkForObjects=True

                for eachpax in personcheck:
                    # get body part coordinates
                    bodyDetectionpoints = checkbody(detectionImage, eachpax)
                    
                    #body part pairs to dictionary
                    dictBodyPart = checkCoordinates(bodyDetectionpoints) 
                    # send image for detection based on objects referred based on body part
                    if itemDetectionList and dictBodyPart  :
                        for equipmentSelection in itemDetectionList :

                            # head part (Helmet)
                            if equipmentSelection == 14 :
                                # for eachpax in personcheck:
                                detectionResult = checkHardHat (dictBodyPart,detectionImage, eachpax)
                                listtoSerializer.append(detectionResult)

                            # gloves part (gloves)
                            if equipmentSelection == 13 :
                                detectionResult =  checkGloves (dictBodyPart,detectionImage)
                        
                        #detectionResult returns the following:
                        # detectionResult.equipment = 13 or 14
                        # detectionResult.detection = True or False >> detect hardhat or not
                        # detectionResult.coordinates = []  >> hardhat coordinates
                        # detectionResult.partDetection = True or False  >> detect bodyparts or not
                        # listtoSerializer.append(detectionResult)

        
                # if list is not empty
                if listtoSerializer  :

                    #serialize object and set content for return
                    serializer = DetectionsSerializer(listtoSerializer, many=True)
                    content ={"detections": serializer.data , "humanDetections" :  True   }
                else :
                    # error flow return
                    content ={"errorMessage": "Please reposition yourself"  , "humanDetections" :  False  }
            
             # if more than on person is detected
            # elif len(personcheck ) > 1:
            #     content ={"errorMessage": "too many persons detected "  , "humanDetections" :  False  }
            # check for persons only
            elif checkForObjects == False and len(personcheck) >= 1 :
                
                personserializer = PersonCoordSerializer(listtoSerializer2, many=True)
                
                content ={"detections": personserializer.data, "humanDetections" :  True  }
            else :
                # if no human detected
                content ={"errorMessage": "Person not detected"  , "humanDetections" :  False  }
        # if an error occured
        except Exception as ex:
            print( ex)
    else :
        content ={"errorMessage":  "form is invalid" , "humanDetections" :  False   }
    
    # convert dictionary to json
    json_object = json.dumps(content)   
    
    
    # return response
      
    return  HttpResponse(json_object, content_type='text/json')


# def run_detection(frame):
#     Width = frame.shape[1]
#     Height = frame.shape[0]

#     scale = 1/255
#     classNames=['helmet ONLY', 'person with helmet', 'ALERT!', 'person']
#     # classFile = "C:\\Users\\Common\\Downloads\\TestDetection\\coco2.names"#    with open(classFile, 'rt') as f:
#     #     classNames = f.read().rstrip('\n').split('\n')
            
#     configPath = "C:\\Users\\Common\\Downloads\\yolov3.weights"
#     weightsPath = "C:\\Users\\Common\\Downloads\\yolov3.cfg"

#     net = cv2.dnn.readNet(weightsPath, configPath)

#     # create input blob
#     blob = cv2.dnn.blobFromImage(frame, scale, (416,416), (0,0,0), True, crop=False)

#     # set input blob for the network
#     net.setInput(blob)

#     # run inference through the network and gather predictions from output layers
#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#     outs = net.forward(output_layers)    

#     # initialization
#     class_ids = []
#     confidences = []
#     boxes = []
#     conf_threshold = 0.7
#     nms_threshold = 0.6

#     # for each detetion from each output layer get the confidence, class id, 
#     # bounding box params and ignore weak detections (confidence < 0.5)
#     for out in outs:
#         for detection in out:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.5:
#                 center_x = int(detection[0] * Width)
#                 center_y = int(detection[1] * Height)
#                 w = int(detection[2] * Width)
#                 h = int(detection[3] * Height)
#                 x = center_x - w / 2
#                 y = center_y - h / 2
#                 class_ids.append(class_id)
#                 confidences.append(float(confidence))
#                 boxes.append([x, y, w, h])

#     # apply non-max suppression
#     indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

#     # go through the detections remaining after nms and draw bounding box
#     for i in indices:
#         i = i[0]
#         box = boxes[i]
#         x = box[0]
#         y = box[1]
#         w = box[2]
#         h = box[3]

#         #draw_bounding_box(frame, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
#         # Draw bounding boxes
#         label = str(classNames[class_id])
#         #color = COLORS[class_id]
#         cv2.rectangle(frame, (round(x), round(y)), (round(x+w), round(y+h)), (255,0,0), 2)
#         cv2.putText(frame, label, (round(x) - 10, round(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

#     return frame
