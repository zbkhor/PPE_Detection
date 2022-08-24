# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from rest_framework import serializers
from SafetyManagerApp.models import equipment


class AccessTokenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tokenStr =  serializers.CharField(max_length=100)  
    isValid = serializers.BooleanField(default=True) 
     
 