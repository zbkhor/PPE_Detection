# Author: Tharine Ramachandran
# Data Written: 10/08/2020
import codecs 
from bson import ObjectId
from rest_framework import status
from SafetyManagerApp.forms  import ChannelsForm,ChannelsUpdateForm,LogDeleteForm
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from SafetyManagerApp.models import channel, accesstoken
from .serializers import ChannelsSerializer 


class ChannelView(APIView):
    # get method to retrieve channel data
    def get(self, request,pk = None):
       try :
        # single record by id
        if pk:
            # get record or raise error
            channels= get_object_or_404(channel.objects.all(), pk=pk)
            channels.tokenStr = 'xoxb-xxxxxxxxxx-xxxxxx-'+channels.tokenStr[-4:]
            # initialze serializer
            serializer = ChannelsSerializer(channels)

            # return success response with data
            content = {"Success": serializer.data}
            return Response (content ,status=status.HTTP_200_OK )

        # get all records of channel
        channels = channel.objects.all()
        for channelsLog in channels :
            channelsLog.tokenStr = 'xoxb-xxxxxxxxxx-xxxxxx-'+channelsLog.tokenStr[-4:]
        # initialze serializer with records
        serializer = ChannelsSerializer(channels, many=True)

        # return success response with data
        content = {"Success": serializer.data}
        return Response (content ,status=status.HTTP_200_OK )

       except :
           # return error response  
           content = {"Error":"Error while retrieve channel data"}
           return Response (content ,status=status.HTTP_400_BAD_REQUEST )
  
  # delete method to remove record channel record
    def delete(self, request)  :        # initialize form to request data and variables
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
                        deletechannel = channel.objects.get(pk=i) 
                        # delete record 
                        deletechannel.delete()  

                    except channel.DoesNotExist:
                        # record channel id if error occured
                        error.append(i)                   

            except :          
                # return error response
                content = {"Error":"Error while deleting channel data"}
                return Response (content ,status=status.HTTP_400_BAD_REQUEST )
            if len(error) > 0 :
                # return error response for failed deletion of records
                content = { "Error" :  'Channels of the following could not be deleted '+  ",".join("{0}".format(i) for i in error) }
                return Response (content ,status=status.HTTP_400_BAD_REQUEST )
            else :
                # return success response
                content = {'Success': 'Channels were successfully deleted'  }
                return Response(content,status=status.HTTP_200_OK) 

        else :
            # return error response if form is invalid
            content = {"Error":"Form invalid. Add an access token " }
            return Response (content ,status=status.HTTP_400_BAD_REQUEST )

     # post method to create new channel record
    def post(self, request):        
        # initialize form to request data
         form = ChannelsForm(request.POST ) 
         # check if form is valid
         if form.is_valid():
             try :
                 # initialize from form to variables
                 formChannelStr =form.cleaned_data['channelStr']
                 formIsValid=form.cleaned_data['isValid']
                 formtokenStr=form.cleaned_data['tokenStr'] 
                 accesstokenobject = accesstoken.objects.get(pk=formtokenStr) 
                 formtokenStr = accesstokenobject.tokenStr
                 # check for duplicates before creating new form 
                 duplicates = channel.objects.filter(channelStr=formChannelStr,tokenStr=formtokenStr)

                 if duplicates.exists(): 
                     # return error response if a duplicate is found
                      content = {"Error": "This channel already exists"}
                      return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                 else :
                     # check if accesstoken is valid and is in database 
                     accesstokenExists = accesstoken.objects.filter(tokenStr=formtokenStr,isValid = True )
                     
                     if accesstokenExists.exists() :
                         # create new channel object 
                         channelObj = channel () 
                         # initialize variables
                         channelObj.channelStr = formChannelStr
                         channelObj.isValid = formIsValid
                         channelObj.tokenStr = formtokenStr
                         # save record to database
                         channelObj.save()
                     else :
                         content = {"Error": "This channel does not contain a valid access token"}
                         return Response (content ,status=status.HTTP_400_BAD_REQUEST )

                     # return success response
                     content = {"Success": "Channel has been added" }
                     return Response(content)

             except :
                # return error response
               content = {"Error": "Error occured while retrieving the data" }
               return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                           
         else : 
             # return error response if form is invalid
              content = {"Error":"Form invalid. Add an Channel Name "}
              return Response (content ,status=status.HTTP_400_BAD_REQUEST    )              
     
          
    # put method to update records
    def put(self, request):        
        # initialize form to request data
         form = ChannelsUpdateForm(request.POST ) 
         # check if form is valid
         if form.is_valid():
             try :
                 # initialize from form to variables
                 formChannelStr =form.cleaned_data['channelStr']
                 formIsValid=form.cleaned_data['isValid']
                 formtokenStr=form.cleaned_data['tokenStr']
                 
                 accesstokenobject = accesstoken.objects.get(pk=formtokenStr) 
                 formtokenStr = accesstokenobject.tokenStr

                 formid =  int (form.cleaned_data['id']) 
                 try:
                     channelObj = channel.objects.get(id=formid)
                     # initialize variables
                     if  formIsValid  is not None:
                         channelObj.isValid = formIsValid

                     if  formChannelStr  is not 'None':
                         channelObj.channelStr = formChannelStr

                     if  formtokenStr  is not 'None':
                         accesstokenExists = accesstoken.objects.filter(tokenStr=formtokenStr,isValid = True )
                         if accesstokenExists.exists() :
                             channelObj.tokenStr = formtokenStr 
                         else :
                             content = {"Error": "This channel does not contain a valid access token or is not active"}
                             return Response (content ,status=status.HTTP_400_BAD_REQUEST )


                     # check for duplicates before updating new form 
                     duplicates = channel.objects.filter(channelStr= channelObj.channelStr,tokenStr=channelObj.tokenStr ,isValid = channelObj.isValid   )

                     if duplicates.exists():
                         # return error response if a duplicate is found
                         content = {"Error": "This channel already exists"}
                         return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                     else :
                         # check if accesstoken is valid and is in database 
                         channelObj.save()
                         # return success response
                         content = {"Success": "Channel has been updated" }
                         return Response(content)
                             
                             
                 except channel.DoesNotExist:
                     content = {"Error": "This channel does not contain a valid channel id"}
                     return Response (content ,status=status.HTTP_400_BAD_REQUEST ) 
                       
             except Exception as ex:
                 # return error response
                 content = {"Error": "Error occured while retrieving the data" }
                 return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                           
         else : 
             # return error response if form is invalid
             content = {"Error":"Form invalid. Add an channel name or access token "}
             return Response (content ,status=status.HTTP_400_BAD_REQUEST    )              
          