# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from rest_framework import serializers
 

class tf2Serializer(serializers.Serializer):

    time = serializers.CharField()  
    ObjectViolated = serializers.CharField()
    condition  = serializers.CharField()
    id = serializers.IntegerField() 
    image = serializers.CharField() 
    # compliant= serializers.BooleanField()
     
     
     

 