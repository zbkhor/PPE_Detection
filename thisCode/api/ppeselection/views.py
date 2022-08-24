# Author: Tharine Ramachandran
# Data Written: 10/08/2020
import codecs
import random
from bson import ObjectId

import logging
from rest_framework import status

from SafetyManagerApp.forms  import PPESelectionForm
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from SafetyManagerApp.models import ppeselection , equipmentList
from .serializers import PPESelectSerializer  
from rest_framework.decorators import action, api_view   


# Initialize variables for equipment list
equipmentListVal = equipmentList()
equipmentDict = equipmentListVal.equipmentDict()


class PPESelectView(APIView):
    # get method for retrieving details of PPE selection
    def get(self, request,pk = None):
        try :
            # getting details for single record
            if pk:
                try :
                    # get ppe selection log by id 
                    ppeSelectionLogs =  ppeselection.objects.get(pk=pk)

                    ## convert ppeselection equipment to list
                    #listPpe = list(ppeSelectionLogs.selectionEquipment)
                    ## get equipement name string based on list of ppe id 
                    #selectionEquipment = get_object_string (listPpe)
                    ## initialize ppe selection string to object 
                    #ppeSelectionLogs.selectionEquipment = selectionEquipment 

                     # initialize ppe selection query object to serializer object
                    serializer = PPESelectSerializer(ppeSelectionLogs) 
                    # return success response
                    content = { "Success" : serializer.data}
                    return Response( content ,status=status.HTTP_200_OK)
                except ppeselection.DoesNotExist:
                    #return error response
                    content = { "Error" : "Record of this PPE selection is not found"}
                    return Response( content ,status=status.HTTP_400_BAD_REQUEST)


            else :
                # get all ppe selection log 
                ppeSelectionLogs = ppeselection.objects.all()

                #for log in ppeSelectionLogs:
                #    # convert ppeselection equipment to list
                #    listPpe = list(log.selectionEquipment)
                #    # get equipement name string based on list of ppe id 
                #    selectionEquipment = get_object_string (listPpe)
                #    # initialize ppe selection string to object 
                #    log.selectionEquipment = selectionEquipment

                # initialize ppe selection query objects to serializer objects
                serializer = PPESelectSerializer(ppeSelectionLogs, many=True)  
                # return success response
                content = { "Success" : serializer.data}
                return Response( content ,status=status.HTTP_200_OK)
        except :
            # return error response
            content = { "Error": "Failed to retrieve records"}
            return Response ( content, status = status.HTTP_400_BAD_REQUEST)


# delete method to remove PPE Selection
    def delete(self, request,pk)  :
        try :
            # check if PPE selection exists
            ppeSelectionLogs = ppeselection.objects.filter(id=pk)

            if ppeSelectionLogs.exists():
                # get single  ppe record  and delete
                ppeSelectionLogs = get_object_or_404(ppeselection.objects.all(), pk=pk) 
                ppeSelectionLogs.delete() 
                # return success response
                content = { "Success" : 'Successfully deleted PPE selection' } 
                return Response(content,  status=status.HTTP_200_OK)
                
            else :
                # return if ppe selection does not exists
                content = { "Error": "PPE Selection has already been deleted" }
                return Response(content ,status=status.HTTP_400_BAD_REQUEST)
                 
        except :
            # return if error occurs
            content = { "Error": "Error occured" }
            return Response(content,  status=status.HTTP_400_BAD_REQUEST)

             
# post method to create ppe selection 
    def post(self, request):        
        # initialize form and get post details
         form = PPESelectionForm(request.POST) 
         #check if form is valid
         if form.is_valid():
             try :
                 # initialize  selection equipment
                 formEquipment = form.cleaned_data['selectionEquipment']   
                  # create ppeselection object and initialize variables

                 duplicates = ppeselection.objects.first()

                 if duplicates:
                     duplicates.selectionEquipment = formEquipment
                     duplicates.save()
                 else :

                     ppeSelectionObj = ppeselection() 
                     ppeSelectionObj.selectionEquipment = formEquipment
                     # create new ppe selection record
                     ppeSelectionObj.save()
                     # return success message

                 content = { "Success" :  "PPE selection has been saved." }
                 return Response(content,  status=status.HTTP_200_OK)

             except Exception as e: 
                 # return error response
                 content = { "Error": e }
                 return Response(content,  status=status.HTTP_400_BAD_REQUEST)
             
         else : 
             # return if form is not valid
              content = { "Error":"Form invalid. PPE equipment selection "}
              return Response(content,  status=status.HTTP_400_BAD_REQUEST)

## method that takes array of equipement id and returns a string of the equipement name from the array
#def get_object_string (objectList): 
#    #initialize array to store equipement name 
#    objectNameArr = []
#    try :
#        for i in objectList:
#            # get equipment name using the id from equipment dictionary
#            objectName =  equipmentDict.get(int(i))
#            # insert name to array
#            objectNameArr.append(objectName)
#        # if no name is detected
#        if not objectNameArr:
#            strObjects = "None Detected"  
#        #  returns a string of equipment name separated by comma 
#        strObjects = ",".join("{0}".format(name) for name in objectNameArr)
        
       
#    except :
#        #  error message 
#        strObjects = "An error occurred while retrieving PPEequipment details"
#    # return message  
#    return strObjects

# GET
# Retrieves the latest ppe selection
@api_view()
def get_selection (request) :
    try :
        # get latest ppe selection 
        latest = ppeselection.objects.latest('timestamp')

        ## convert ppeselection equipment to list
        #listPpe = list(latest.selectionEquipment)
        ## get equipement name string based on list of ppe id 
        #selectionEquipment = get_object_string (listPpe)
        ## initialize ppe selection string to object 
        #latest.selectionEquipment = selectionEquipment 
        # initialize ppe selection query object to serializer object

        serializer = PPESelectSerializer(latest)
        # return success response 
        content = { "Success" :  serializer.data}
        return Response(content,  status=status.HTTP_200_OK)
    except Exception as ex:
        # return error response
        content = { "Error": "An error occurred while retrieving PPE selection details"}
        # content = { "Error": str(ex)}
        return Response(content,  status=status.HTTP_400_BAD_REQUEST)
