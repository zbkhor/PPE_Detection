# Author: Tharine Ramachandran
# Data Written: 10/08/2020
import datetime    
from rest_framework.response import Response
from rest_framework.views import APIView  
from rest_framework.decorators import action, api_view   
from datetime import datetime, timedelta ,date
import pytz
from rest_framework import status 
import slack
from SafetyManagerApp.models import accesstoken , channel
from SafetyManagerApp.forms  import sendMessageForm

@api_view()
def send_message(request):
    #initialize form
    form = sendMessageForm(request.POST) 
    #check if form is valid
    if form.is_valid():
        try :
            # get all slack credentials 
            text = form.cleaned_data['text']  
            channels = channel.objects.filter(isValid =True)
            # publish message 
            for channelLog in channels :
                client = slack.WebClient(token= channelLog.tokenStr)
                client.chat_postMessage(channel= channelLog.channelStr, text=text )
            # return success message 
            content = { "Success": "Message sent to safety manager "}
            return Response ( content, status = status.HTTP_200_OK)
        except :
            # return error response incase of error 
            content = { "Error": "Error occured while sending message"}
            return Response ( content, status = status.HTTP_400_BAD_REQUEST)
    else :
        # return error response incase of invalid from
        content = { "Error": "Form is invalid a text"}
        return Response ( content, status = status.HTTP_400_BAD_REQUEST)        
    




