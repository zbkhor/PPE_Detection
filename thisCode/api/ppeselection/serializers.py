# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from rest_framework import serializers
from SafetyManagerApp.models import equipment


class PPESelectSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    timestamp =  serializers.DateTimeField()  
    selectionEquipment =  serializers.ListField(child = serializers.IntegerField()) 
    # selectionEquipment = serializers.JSONField(child = serializers.CharField(max_length = 100))
    # selectionEquipment = serializers.ListField()

     

 