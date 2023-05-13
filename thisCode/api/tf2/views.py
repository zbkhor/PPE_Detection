# Author: Tharine Ramachandran
# Data Written: 10/08/2020
import codecs
import datetime 
from bson import ObjectId

import pymongo
import gridfs
from pymongo import MongoClient
import os 
from rest_framework import status
from SafetyManagerApp.forms  import ImageUploadForm,LogDeleteForm,TestForm
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView 
from SafetyManagerApp.models import details, log, equipmentList,tensorflow2,conditionList

from .serializers import tf2Serializer 
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
import requests
import numpy as np 
import cv2 as cv
import os
import io
import base64
from PIL import Image 
  
# Initialize equipment dictionary
equipmentListInt = equipmentList()
equipmentDict = equipmentListInt.equipmentDict()
conditionDict = conditionList().conditionDict()
equipmentIdDict = equipmentListInt.equipmentIdDict()
conditionIdDict = conditionList().conditionIdDict()
url = './api/detection/tf2/'

class tf2View(APIView):
    def get(self, request):

        #initialize variables
        items = [] 

        # get all records of logs
        alllogs = tensorflow2.objects.all()

        try :            

            for eachLog in alllogs:

                if eachLog :

                    # create new details object and ppe equipment list 
                    viewlog = details()
                    ppeequipment = []

                    # get time and date from timestamp and convert to string
                    date = eachLog.time.strftime("%d-%m-%y") 
                    time =eachLog.time.strftime("%H:%M") 

                    # initialize variables
                    viewlog.id = eachLog.id
                    viewlog.time = "{0} , {1}".format(date , time)   
                    viewlog.image = eachLog.image
                  
                    # convert variable to list
                    listObjectViolated = list(eachLog.ObjectViolated) 
                    listcondition = list(eachLog.condition)
                    
                    # #checks if log was compliant
                    # if listobjectsViolated :
                    #     viewlog.compliant = False
                    #     listcondition = list(eachLog.condition)  + listobjectsViolated
                    # else :
                    #     viewlog.compliant = True
                    #     listcondition = list(eachLog.condition)  

                    #  get names of equipment from id
                    viewlog.ObjectViolated= getobjectstring (listObjectViolated)
                    viewlog.condition= getconditionstring (listcondition)

                    # initialize image base64 code to object         
                    # viewlog.image=eachLog.image  
                    # add object to list
                    items.append(viewlog) 

        except Exception as ex: 
            # return error response incase of error
            # content = {"Error":"Error while retrieving log data"}
            content = {"Error": str(ex)}
            return Response (content ,status=status.HTTP_400_BAD_REQUEST )

        # initialze serializer with records
        serializer = tf2Serializer(items, many=True)

        # return succes response
        content ={"Success": serializer.data}
        return Response(content,status=status.HTTP_200_OK)

     # delete method to remove record
    def delete (self, request):
        # initialize form to request data and variables
        form = LogDeleteForm(request.POST)        
        error = []

        # check if form is valid
        if form.is_valid():
            try :
                #get a list of record ids
                record = form.data.getlist('id')
                for i in record :                     
                    try:
                        # get record by id
                        deletelog = tensorflow2.objects.get(pk=i)
                        # get image id
                        logimage = deletelog.image 
                        # delete record 
                        deletelog.delete() 

                    except log.DoesNotExist:
                        # record log id if error occured
                        error.append(i)                   

            except :          
                # return error response
                content = {"Error":"Error while deleting log data"}
                return Response (content ,status=status.HTTP_400_BAD_REQUEST )
            if len(error) > 0 :
                # return error response for failed deletion of records
                content = { "Error" :  'Logs of the following could not be deleted '+  ",".join("{0}".format(i) for i in error) }
                return Response (content ,status=status.HTTP_400_BAD_REQUEST )
            else :
                # return success response
                content = {'Success': 'Logs were successfully deleted'  }
                return Response(content,status=status.HTTP_200_OK)

  
    def post(self, request):        
        #initialize variables of form
         form = TestForm(request.POST, request.FILES) 

         if form.is_valid():


             # image for cropping 
            #  image = imageCropping(top,left,width,height,imagestr)
             # get violated and detected values
             image = form.cleaned_data['image']  
             ObjectViolated = form.cleaned_data['ObjectViolated']
             condition = form.cleaned_data['condition']   
            #  objectsViolated = form.cleaned_data['objectsViolated']   
             # time of violation
             time = datetime.datetime.now()

             try :
              # create log object to store details  
                 logentry = tensorflow2()
                 logentry.image= image 
                #  logentry.objectsViolated = objectsViolated 
                #  logentry.condition = condition
                 logentry.ObjectViolated= getobjectid(ObjectViolated) 
                 logentry.condition= getconditionid(condition) 
                 
                 logentry.time = time
                 #save log to database
                 logentry.save()

                 if logentry.ObjectViolated != '{14}':
                     #return success response
                     content = {"Success": logentry.ObjectViolated} 
                     return Response (content ,status=status.HTTP_200_OK )
                 elif logentry.ObjectViolated =='{14}':
                     try:

                         date = time.strftime("%d-%m-%y") 
                         time =time.strftime ("%H:%M")
                         data = {'text':'A violation as occured at {0} : {1} and the following PPE was violated({2})'.format(date,time,ObjectViolated) } 
                         # Initialize URL
                         baseurl = request.get_host()
                         url = 'http://'+baseurl+'/api/slack/send_message/'
                         # send response5
                         response = requests.get(url, data = data)
                         # check response
                         if response.status_code == 200 :
                             # return success response
                             content = {"Success": ObjectViolated} 
                             return Response (content ,status=status.HTTP_200_OK )
                         else :
                             # raise error if action wasnt successful
                             content = {"Success": "Log is saved and message sent to manager "}
                             error_response = response.content.decode('utf-8')  # Decode the response content to string
                             content["Error"] = error_response
                             return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
                     except :
                         # return error response
                         content = {"Success": logentry.condition } 
                         return Response (content ,status=status.HTTP_400_BAD_REQUEST )

             except Exception as ex:
                # return error response
                # content = { "Error" :  "Error occured" }
                content = { "Error" :  str(ex) }
                return  Response (content ,status=status.HTTP_400_BAD_REQUEST )
             
         else : 
             #  return error response if form is invalid
             content ={"Form is invalid. Add an image , violated ppe equipment or  detected ppe equipment"}
             return  Response (content ,status=status.HTTP_400_BAD_REQUEST )

 # method that returns the names of equipement from the list
def getobjectstring (objectlist): 
    stringofobject= []
    for i in objectlist:
        objectname =  equipmentDict.get(int(i))
        stringofobject.append(objectname)

    strobjects = ", ".join("{0}".format(i) for i in stringofobject)

    if not strobjects:
        strobjects = "None"         

    return strobjects

def getconditionstring (conditionlist): 
    stringofobject= []
    for i in conditionlist:
        conditionname =  conditionDict.get(int(i))
        stringofobject.append(conditionname)

    strobjects = ", ".join("{0}".format(i) for i in stringofobject)

    if not strobjects:
        strobjects = "None"         

    return strobjects


def getconditionid (objectname): 

        objectname =  conditionIdDict.get(objectname)
        objectname = "{"+str(objectname)+"}"
        return objectname

def getobjectid (objectname): 
        objectname =  equipmentIdDict.get(objectname)
        objectname = "{"+str(objectname)+"}"
        return objectname
# returns the details of a specific log
class LogDetailView(APIView):
    def get(self, request, pk):

        try :
            # get log details
                eachLog = log.objects.get(pk=pk)

                # intialze variables to object 
                viewlog = details()
 
                date = eachLog.time.strftime("%d-%m-%y") 
                time =eachLog.time.strftime("%H:%M") 

                viewlog.id = eachLog.id
                viewlog.time = time 
                viewlog.date = date 

                listobjectsViolated = list(eachLog.objectsViolated)
                listcondition = list(eachLog.condition)

                viewlog.objectsViolated = getobjectstring (listobjectsViolated)
                viewlog.condition = getobjectstring (listcondition)        
                viewlog.image=eachLog.image   
                # initalize to log serializer
                serializer = tf2Serializer(viewlog)
                # return success response
                content = {"Success": serializer.data }
                return Response(content,status=status.HTTP_200_OK )

        except:
            # return error response
            content = {"Error" : "Error occured"}
            return Response(content,status=status.HTTP_400_BAD_REQUEST )

         
     


