# Author: Tharine Ramachandran
# Data Written: 10/08/2020
import codecs
import datetime    
from rest_framework.response import Response
from rest_framework.views import APIView  
from rest_framework.decorators import action, api_view   
import time
import json  
import subprocess
import os
from datetime import datetime
import datetime
from django.http import JsonResponse,HttpResponse 
import shutil
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import csv 
from SafetyManagerApp.models import details, log, equipmentList,tensorflow2
import json
from api.tf2.views import getobjectstring,getobjectid,getconditionid,getconditionstring
import csv, io,sys
 
# Initialize equipment dictionary
equipmentListInt = equipmentList()
equipmentDict = equipmentListInt.equipmentDict()
equipmentIdDict= equipmentListInt.equipmentIdDict()
def getEquipmentID( equipmentStr) :
    equipmentIDList=[]
    equipmentNameArray = equipmentStr.split(',') 
    for equipmentName in equipmentNameArray:
        equipmentIDList.append(equipmentIdDict[equipmentName.strip() ])
    return equipmentIDList

def getTime(timeStr):

    timeValue =   datetime.datetime.now()
    timeArray = timeStr.split(',') 
    array = 0
    for x in timeArray:
        x.strip()
        array+=1
    logDate = timeArray[0]
    logTime = timeArray[-1]
    timeValue = datetime.datetime.strptime(logDate+" "+logTime,'%d-%m-%y %H:%M')

    return timeValue

def getLogs():
    # get all records of logs
    alllogs = tensorflow2.objects.all()
    items=[]
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
        print(ex)

    return items

@csrf_exempt
def db_export(request):
    try :

        listLogs = getLogs()
        if listLogs:
            with open('logs.csv', 'w', newline="") as file:
                fieldnames = ['id', 'time','compliant', 'ObjectViolated','condition', 'image' ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for log in listLogs:
                    writer.writerow({'id': log.id, 'compliant': log.compliant, 'condition': log.condition,'ObjectViolated': log.ObjectViolated, 'time': log.time, 'image': log.image}) 

            with open('logs.csv') as file:
               response = HttpResponse(file, content_type='text/csv')
               response['Content-Disposition'] = 'attachment; filename=logs.csv'
            return response
        
    except Exception as ex:
        print (ex)
    content = {"Error" : "Error occured"}
    return HttpResponse(content, content_type='application/json')
 

@csrf_exempt
@api_view(('POST','GET'))
def db_import(request):
    # try :
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            content = {"Error" : "File is not a CSV file"}
            return Response(content,status=status.HTTP_400_BAD_REQUEST ) 
 
        data_set =   csv_file.read().decode('UTF-8-sig')
        io_string = io.StringIO(data_set) 
        header =  [x.lower() for x in next(csv.reader(io_string))]        
        keyList = ['time' ,'objectviolated','condition','image']
        csvcolumnKeys = {}
        csv.field_size_limit(100000000) 

        # try :
        for key in keyList:
            csvcolumnKeys[key] = header.index(key)
        for column in csv.reader(io_string):
            if column  :
                logentry = tensorflow2()
                logentry.image= column[csvcolumnKeys['image']] 
                if column[csvcolumnKeys['objectviolated']] !='None': 
                    logentry.ObjectViolated = getobjectid(column[csvcolumnKeys['objectviolated']] )
                else : 
                    logentry.ObjectViolated =[]
                if column[csvcolumnKeys['condition']]!= 'None' : 
                    logentry.condition = getconditionid( column[csvcolumnKeys['condition']] )
                else : 
                    logentry.condition =[]
                     
                logentry.time = getTime(column[csvcolumnKeys['time']])
                logentry.save()


    #     except Exception as ex:
    #         content = {"Error" : "An error while creating the logs"}
    #         return Response(content,status=status.HTTP_400_BAD_REQUEST )
    # except Exception as ex:
    #     content = {"Error" : "An error occurred while accessing the file."}
    #     return Response(content,status=status.HTTP_400_BAD_REQUEST )

        content = {"Success" : "Logs were successfully exported"}
        return Response(content,status=status.HTTP_200_OK)

