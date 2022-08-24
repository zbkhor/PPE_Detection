import codecs
import datetime    
from rest_framework.response import Response
from rest_framework.views import APIView 
from SafetyManagerApp.models import log, details, equipmentList, equipment
from rest_framework.decorators import action, api_view   
from datetime import datetime, timedelta ,date
import pytz
from rest_framework import status
 

@api_view()
# gets the total number of logs 
def total_logs(request):
    totalLogs = 0
    allLogs = log.objects.all( )
    totalLogs = len(allLogs)

    content = { "total ": totalLogs } 
    return Response (content ,status=status.HTTP_200_OK    )


 