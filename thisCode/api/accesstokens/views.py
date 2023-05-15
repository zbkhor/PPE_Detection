# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from SafetyManagerApp.forms  import AccessTokenForm,LogDeleteForm,AccessTokenUpdateForm
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from SafetyManagerApp.models import accesstoken,channel
from .serializers import AccessTokenSerializer 
from rest_framework import status
import requests 
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
class AccessTokenView(APIView):
        # get method to retrieve channel data

    def get(self, request,pk = None):
        try:
            # single record by id
            if pk:
                # get record or raise error
                accessTokens = get_object_or_404(accesstoken.objects.all(), pk=pk)


                accessTokens.tokenStr = accessTokens.tokenStr[-4:]


                # initialze serializer
                serializer = AccessTokenSerializer(accessTokens)
                # return success response with data
                content = {"Success": serializer.data}
                return Response (content ,status=status.HTTP_200_OK )

            # get all records of accesstoken
            accessTokens = accesstoken.objects.all()

            for accessTokenLog in accessTokens :
                 accessTokenLog.tokenStr = 'xoxb-xxxxxxxxxx-xxxxxx-'+accessTokenLog.tokenStr[-4:]

            # initialze serializer with records
            serializer = AccessTokenSerializer(accessTokens, many=True)

            # return success response with data
            content = {"Success": serializer.data}
            return Response (content ,status=status.HTTP_200_OK )

        except :
            # return error response  
            content = {"Error":"Error while retrieve access token data"}
            return Response (content ,status=status.HTTP_400_BAD_REQUEST )
  
 
  # delete method to remove accesstoken channel record
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
                        deleteaccesstoken = accesstoken.objects.get(pk=i) 
                        channelUses = channel.objects.filter( tokenStr=deleteaccesstoken.tokenStr)
                        if channelUses.exists():
                            content = {"Error":"There is channel using this token, therefore it cannot be deleted"}
                            return Response (content ,status=status.HTTP_400_BAD_REQUEST )
                        else :
                            # delete record 
                            deleteaccesstoken.delete()  

                    except accesstoken.DoesNotExist:
                        # record accesstoken id if error occured
                        error.append(i)                   

            except :          
                # return error response
                content = {"Error":"Error while deleting access token data"}
                return Response (content ,status=status.HTTP_400_BAD_REQUEST )
            if len(error) > 0 :
                # return error response for failed deletion of records
                content = { "Error" :  'Access token of the following could not be deleted '+  ",".join("{0}".format(i) for i in error) }
                return Response (content ,status=status.HTTP_400_BAD_REQUEST )
            else :
                # return success response
                content = {'Success': 'Access token were successfully deleted'  }
                return Response(content,status=status.HTTP_200_OK)
        else :
           # return error response if form is invalid
           content = {"Error":"Form invalid. Add an access token ID" }
           return Response (content ,status=status.HTTP_400_BAD_REQUEST )



    def post(self, request):        
         
        # initialize form to request data
         form = AccessTokenForm(request.POST ) 

         # check if form is valid
         if form.is_valid():
             try :

                 # initialize from form to variables
                 formtokenStr =form.cleaned_data['tokenStr']
                 formIsValid=form.cleaned_data['isValid']
                 
                 # check for duplicates before creating new form 
                 duplicates = accesstoken.objects.filter(tokenStr=formtokenStr)

                 if duplicates.exists():
                     # return error response if a duplicate is found
                     content = {"Error":"This access token already exists" }
                     return Response (content ,status=status.HTTP_400_BAD_REQUEST )
                 
                 else :
                      
                     # api-endpoint 
                     URL = "https://slack.com/api/auth.test" 
  
                     # defining a params dict for the parameters to be sent to the API 
                     PARAMS = {'token':formtokenStr} 
  
                     # sending get request and saving the response as response object 
                     requestResult = requests.get(url = URL, params = PARAMS) 
  
                     # extracting data in json format 
                     data = requestResult.json() 
  
  
                     # extracting latitude, longitude and formatted address  
                     # of the first matching location 
                     isValidtoken = data['ok'] 

                     if isValidtoken == True:
                         # create new access token  object 
                         accesstokenObj = accesstoken () 
                         # initialize variables
                         accesstokenObj.tokenStr = formtokenStr
                         accesstokenObj.isValid = formIsValid
                         # save record to databse
                         accesstokenObj.save()

                         # return success response
                         content = {"Success": "Access Token has been added" }
                         return Response (content ,status=status.HTTP_200_OK )
                     else :
                         # return error response
                         content = {"Error":"Token is not a valid token" }
                         return Response (content ,status=status.HTTP_400_BAD_REQUEST )

             except :
                 # return error response
                 content = {"Error":"Error occured while creating an access token" }
                 return Response (content ,status=status.HTTP_400_BAD_REQUEST )
      
         else :
             # return error response if form is invalid
             content = {"Error":"Form invalid. Add an access token details " }
             return Response (content ,status=status.HTTP_400_BAD_REQUEST )

    def put(self, request):        
        # initialize form to request data
         form = AccessTokenUpdateForm(request.POST ) 
         # check if form is valid
         if form.is_valid():
             try :
                 # initialize from form to variables 
                 formIsValid=form.cleaned_data['isValid']
                 formtokenStr=form.cleaned_data['tokenStr']
                 formid =  int (form.cleaned_data['id']) 
                  
                 # check for duplicates before creating new form 
                 duplicates = accesstoken.objects.filter( tokenStr=formtokenStr,isValid = formIsValid)

                 if duplicates.exists(): 
                     # return error response if a duplicate is found
                      content = {"Error": "This access token already exists"}
                      return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                 else :
                    try:
                        # create new access token  object 
                        accesstokenObj = accesstoken.objects.get(id=formid)
                        # initialize variables 
                        if  formIsValid  is not None:
                            accesstokenObj.isValid = formIsValid
                        if formtokenStr :
                            # api-endpoint 
                            URL = "https://slack.com/api/auth.test" 
                            # defining a params dict for the parameters to be sent to the API 
                            PARAMS = {'token':formtokenStr} 
  
                            # sending get request and saving the response as response object 
                            requestResult = requests.get(url = URL, params = PARAMS) 
  
                            # extracting data in json format 
                            data = requestResult.json() 
  
  
                            # extracting latitude, longitude and formatted address  
                            # of the first matching location 
                            isValidtoken = data['ok'] 
                        
                            if isValidtoken == True:
                                accesstokenObj.tokenStr = formtokenStr
                            else :
                                # return error response
                                content = {"Error":"Token is not a valid token" }
                                return Response (content ,status=status.HTTP_400_BAD_REQUEST ) 


                            # save record to database 
                        accesstokenObj.save()
                         
                    except accesstoken.DoesNotExist:
                        content = {"Error": "This access token does not contain a valid channel id"}
                        return Response (content ,status=status.HTTP_400_BAD_REQUEST )
                          
                    # return success response
                    content = {"Success": "Access token has been updated" }
                    return Response(content)

             except Exception as ex:
                # return error response
               content = {"Error": "Error occured while retrieving the data" }
               return Response (content ,status=status.HTTP_400_BAD_REQUEST    )
                           
         else : 
             # return error response if form is invalid
              content = {"Error":"Form invalid. Add an access token name and validity "}
              return Response (content ,status=status.HTTP_400_BAD_REQUEST    )              
 

@api_view(['GET',   ])
def getValidAccessToken(request):
        try:

            # get all records of accesstoken
            accessTokens = accesstoken.objects.filter(isValid = True)

            for accessTokenLog in accessTokens :
                 accessTokenLog.tokenStr = 'xoxb-xxxxxxxxxx-xxxxxx-'+accessTokenLog.tokenStr[-4:]

            # initialze serializer with records
            serializer = AccessTokenSerializer(accessTokens, many=True)

        except :
            # return error response  
            content = {"Error":"Error while retrieve access token data"}
            return Response (content ,status=status.HTTP_400_BAD_REQUEST )
        
        # return success response with data
        content = {"Success": serializer.data}
        return Response (content ,status=status.HTTP_200_OK )
 