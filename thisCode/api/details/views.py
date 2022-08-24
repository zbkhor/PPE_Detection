# Author: Tharine Ramachandran
# Data Written: 10/08/2020
import codecs
import datetime    
from rest_framework.response import Response
from rest_framework.views import APIView 
from SafetyManagerApp.models import log, details, equipmentList, equipment,tensorflow2
from rest_framework.decorators import action, api_view   
from datetime import datetime, timedelta ,date
import pytz
from rest_framework import status

# getting timestamps for dates and converting them to string
startDate = date.today() + timedelta(1)
endDate = date.today() - timedelta(5)

startDateStr = startDate.strftime("%Y-%m-%d")
endDateStr = endDate.strftime("%Y-%m-%d") 

# getting a list of all the days present in the 5 day period from the present day 
date_list = [datetime.now() - timedelta(days=x) for x in range(5)]

# Initialize variables for equipment dic
equipmentListInt = equipmentList()
equipment_dict = equipmentListInt.equipmentDict()

# all logs that occur in the range of the past 5 days


@api_view()
# gets the total number of logs 
def total_logs(request):
    totalLogs = 0
    allLogs = tensorflow2.objects.all()
    totalLogs = len(allLogs)

    content = { "total": totalLogs } 
    return Response (content ,status=status.HTTP_200_OK    )

@api_view()
# get values for chart of the total violation in the past 5 days (series 1) and types of violation in the past 5 days (series 2)
def total_violation(request):
     #  Initialize variables
    countMap = {} 
    violatedLogs = []
    seriesDates = []
    totalViolation = []
    allLogs = tensorflow2.objects.filter(time__gte=endDateStr,time__lte=startDateStr)
 
    try : 
        for eachLog in allLogs :
            #get  violated logs  only 
            if not eachLog.ObjectViolated:
                continue
            else :
                # get date of the violated log
                logDate = eachLog.time.strftime("%Y-%m-%d")
                violatedLogs.append(logDate) 
        # gets total number of logs that was violated by dates recorded in the database
        for violatedLog in violatedLogs:
            countMap[violatedLog] = countMap.get(violatedLog, 0) + 1 

        # get the number of violated logs by dates in the range and assigns the value to a list 
        for eachDay in date_list :
             # converts date to string 
            eachDayStr = eachDay.strftime("%Y-%m-%d")
            # add series dates 
            seriesDate = eachDay.strftime("%d-%m-%Y")
            seriesDates.append(seriesDate)
            # checks if the date is present has any violation values on the countMap  
            
            if eachDayStr in countMap :
                value = countMap.get(eachDayStr)
            else :
                value=0
            # updates the list if violation has occured
            totalViolation.append(value) 
        # Initialze values to variable  
        series2 = violations_bytype()
        series1 = {'name' :"series1",'data':totalViolation[::-1] }
        i=0
        while i <=4:
            a = series1['data'][i] - series2[2]['data'][i]
            series1['data'][i] = a
            i += 1
        
            
        
        seriesDates.reverse()
        # return success response
        content = { 'series1': series1  , 'series2' : series2 , 'dates' : seriesDates} 
        return Response (content ,status=status.HTTP_200_OK    )

    except:
        # return error response 
        content = {"Error" :series1}
        return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
    
# method that returns a list of violations by date and type 
def violations_bytype(): 
    # Initialze variables
    violatedLogs = []  
    countMap = {} 
    series2 = []
    allLogs = tensorflow2.objects.filter(time__gte=endDateStr,time__lte=startDateStr)
    # get violated logs
    for eachLog in allLogs:
        if not eachLog.ObjectViolated :
            continue
        else :
             ObjectsViolated_list = list(eachLog.ObjectViolated) 
                 
        for equipementViolated in ObjectsViolated_list :
            # get equipment violated and date 
            equipment = equipment_dict.get(int(equipementViolated))
            logDate = eachLog.time.strftime("%Y-%m-%d")
            # update list with equipement violated and date
            violatedLogs.append((equipment,logDate))
                 
    for i in violatedLogs: 
        # add the total number of violation for each violation by  type and date
        countMap[i] = countMap.get(i, 0) + 1
    # get list of equipments 
    equipment = list(equipment_dict.values())
         
    for eachEquipment in equipment:    
        violation_list = [] 
        for eachDay in date_list:
            # get date for each day of the range and convert to string 
            eachDayStr = eachDay.strftime("%Y-%m-%d")
            # check if the equipment contains a violation on that day and set it's value
            if (eachEquipment,eachDayStr) in countMap:
                violation_list.append(countMap.get((eachEquipment,eachDayStr)))
            else :
                violation_list.append(0)
        #intialize value of dictionary
        eachViolation = {'name' : eachEquipment , 'data' :violation_list[::-1]}
        series2.append(eachViolation)
    # return list of dictionary 
    return   series2 
    # equipment = equipment_dict.get(14)
    
         
   
    # violation_list = [] 
    # for eachDay in date_list:
    #     # get date for each day of the range and convert to string 
    #     eachDayStr = eachDay.strftime("%Y-%m-%d")
    #     # check if the equipment contains a violation on that day and set it's value
    #     if (equipment,eachDayStr) in countMap:
    #         violation_list.append(countMap.get((equipment,eachDayStr)))
    #     else :
    #         violation_list.append(0)
    # #intialize value of dictionary
    # eachViolation = {'name' : equipment , 'data' :violation_list[::-1]}
    # series2.append(eachViolation)
    # # return list of dictionary 
    # return   series2 




  