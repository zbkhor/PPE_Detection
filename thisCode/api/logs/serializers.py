# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from rest_framework import serializers
 

class LogsSerializer(serializers.Serializer):

    image = serializers.CharField() 
    time = serializers.CharField()  
    objectsDetected  = serializers.CharField()
    objectsViolated  = serializers.CharField()
    id = serializers.IntegerField() 
    compliant= serializers.BooleanField()
     
     
     

 