# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from django.shortcuts import render ,redirect
import codecs
import datetime 
import random
from bson import ObjectId
 

import pymongo
import gridfs
from pymongo import MongoClient
import os 
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework import status

from SafetyManagerApp.forms  import ImageUploadForm,EquipmentForm ,EquipmentUpdateForm
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from SafetyManagerApp.models import  equipment,details
from .serializers import EquipmentSerializer  

class EquipmentsView(APIView):
    # Get method for retrieving equipements details
    def get(self, request,pk = None):

        try :
            # get single equipment details 
            if pk: 
                try :
                   # get record  
                    ppeExists = equipment.objects.filter(id=pk)
                     # check if equipment exists and 
                    if ppeExists.exists():
                        # initialze query to a serialzer 
                        serializer = EquipmentSerializer(ppeExists, many=True)
                        # return single equipment details 
                        content = {"Success": serializer.data}
                        return Response( content ,status=status.HTTP_200_OK)                 
                    else :
                        content = {"Error": "This equipment details could not be found" }
                        return Response (content ,status=status.HTTP_400_BAD_REQUEST)
                except:
                     # error handling  response 
                    content = { "Error":"Could not retrieve equipment records"}
                    return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
            else :
                # initialze query to a serialzer 
                ppeEquipment = equipment.objects.all()
                serializer = EquipmentSerializer(ppeEquipment, many=True)
                # return details of all equipment 
                content = {"Success": serializer.data}
                return Response( content ,status=status.HTTP_200_OK)

        except:
            # error handling  response 
            content = { "Error":"Could not retrieve equipment records"}
            return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
  
  
    #def delete(self, request,pk)  :
    #    try :
    #        ppeexists = equipment.objects.filter(id=pk)
    #        if ppeexists.exists():
    #            deletePPE = get_object_or_404(equipment.objects.all(), pk=pk) 
    #            deletePPE.delete() 
    #            content = {'delete': 'success' }
    #            return Response(content)
                 
    #        else :
    #            content = {"delete": "object has already been deleted" }
    #    except :
    #        content = {"Error": "error occured" }


    #    return Response(content)


    # post method to create a new equipment record 
    def post(self, request):        
         # initialize form values 
         form = EquipmentForm(request.POST ) 
         if form.is_valid():
             try :
                 # retrieve form details and initialize  
                 ppeName =form.cleaned_data['equipmentName']
                 ppeIcon = form.cleaned_data['equipmentIcon'] 
                 # check for duplicates 
                 duplicates = equipment.objects.filter(equipmentName=ppeName)
                 # if duplicates exists
                 if duplicates.exists(): 
                     # return error response for duplicates 
                     content = {"Error": "This equipement already exists" }
                     return Response (content ,status=status.HTTP_400_BAD_REQUEST)
                 
                 else :
                     # create equipment object and initialize values 
                     ppeEquipment = equipment () 
                     ppeEquipment.equipmentName = ppeName
                     ppeEquipment.equipmentIcon = ppeIcon
                     # save record 
                     ppeEquipment.save()
                     #return success response after equipment has been added
                     content = {"Success": "This equipement has been added" }
                     return Response (content ,status=status.HTTP_200_OK    )
 
             except :
                 # Error handling response
                  content = { "Error": "Could not create a new record"}
                  return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
         else :
             # Form is invalid response
             content = { "Error":  "Form invalid. Add a PPE Name " }
             return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
 
    def put(self, request):        
        # initialize form to request data
         form = EquipmentUpdateForm(request.POST ) 
         # check if form is valid
         if form.is_valid():
             try :
                 # initialize from form to variables 
                 formequipmentName=form.cleaned_data['equipmentName']
                 formequipmentIcon=form.cleaned_data['equipmentIcon']
                 formid =  int (form.cleaned_data['id']) 
                  
                 # check for duplicates before creating new form 
                 duplicates = equipment.objects.filter( equipmentName=formequipmentName,equipmentIcon = formequipmentIcon)

                 if duplicates.exists(): 
                     # return error response if a duplicate is found
                      content = {"Error": "This equipment already exists"}
                      return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                 else :
                    try:

                            # update new equipment  object 
                            equipmentObj = equipment.objects.get(id=formid)
                            # initialize variables 
                            equipmentObj.equipmentName = formequipmentName
                            equipmentObj.equipmentIcon = formequipmentIcon
                            # save record to database 
                            equipmentObj.save()
                          

                    except equipment.DoesNotExist:
                        content = {"Error": "This equipment does not contain a valid channel id"}
                        return Response (content ,status=status.HTTP_400_BAD_REQUEST )
                          
                    # return success response
                    content = {"Success": "Equipment has been updated" }
                    return Response(content)

             except Exception as ex:
                # return error response
               content = {"Error": "Error occured while retrieving the data" }
               return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                           
         else : 
             # return error response if form is invalid
              content = {"Error":"Form invalid. Add an equipment name and equipment icon name "}
              return Response (content ,status=status.HTTP_400_BAD_REQUEST    )              
          
