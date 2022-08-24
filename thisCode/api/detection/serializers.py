# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from re import search
from rest_framework import serializers
 

class DetectionsSerializer(serializers.Serializer):
    partDetection =  serializers.BooleanField()
    detection  = serializers.BooleanField()
    coordinates  = serializers.ListField()
    equipment = serializers.CharField()
    
    # Lina added
    personcoords = serializers.ListField()
    numofpersons = serializers.CharField()
    # personindex = serializers.CharField()
    # detection = serializers.ListField()
    # partDetection = serializers.ListField()

# Lina added
class PersonCoordSerializer(serializers.Serializer):
    personcoords = serializers.ListField()
    numofpersons = serializers.CharField()
