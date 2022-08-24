# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from rest_framework import serializers
from SafetyManagerApp.models import equipment


class EquipmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    equipmentName =  serializers.CharField()  
    equipmentIcon = serializers.CharField(max_length=100)
     

 