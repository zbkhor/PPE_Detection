# Author: Tharine Ramachandran
# Data Written: 10/08/2020

# from djongo import models
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django import forms
from django.contrib import admin
from django.db.models.fields import CharField,FloatField
from SafetyManagerApp import settings

class equipment(models.Model):
    equipmentName = models.CharField(max_length=100)
    equipmentIcon = models.CharField(max_length=100)
    # objects = models.DjongoManager()
    objects = models.Manager()
  
class condition(models.Model):
    condition = models.CharField(max_length=100)
    objects = models.Manager()
    
class tensorflow2(models.Model):
    time = models.DateTimeField() 
    image = models.TextField() 
    ObjectViolated = ArrayField(models.CharField(max_length=100, blank=True))
    condition= ArrayField(models.CharField(max_length=100, blank=True))
    objects = models.Manager()
    
 
    
class log(models.Model):
    image = models.TextField() 
    time = models.DateTimeField() 
    # objectsDetected = models.ListField()
    # objectsViolated = models.ListField()
    # objects = models.DjongoManager()
    # # objectsDetected= JSONField()
    # # objectsViolated = JSONField()
    objectsDetected= ArrayField(models.CharField(max_length=100, blank=True))
    objectsViolated = ArrayField(models.CharField(max_length=100, blank=True))
    objects = models.Manager()

class accesstoken(models.Model):
    tokenStr = models.CharField(max_length=100) 
    isValid = models.BooleanField(default=True) 
    # objects = models.DjongoManager()
    objects = models.Manager()

class channel(models.Model):
    channelStr = models.CharField(max_length=100) 
    isValid = models.BooleanField(default=True) 
    tokenStr = models.CharField( max_length=100) 
    # objects = models.DjongoManager()
    objects = models.Manager()

class ppeselection(models.Model):
    timestamp =  models.DateTimeField(auto_now=True) 
    # selectionEquipment = models.ListField() 
    # objects = models.DjongoManager()
    # selectionEquipment = JSONField()
    selectionEquipment = ArrayField(models.CharField(max_length=100, blank=True))
    objects = models.Manager()

class details:
    pass

class detectionObject:
    pass

class equipmentList(object):
    def __init__(self):
        self.equipmentList = equipment.objects.values() 

    def equipmentDict(self): 
        equipmentDictionary = {}
        for dict in self.equipmentList:
            id = dict.get('id')
            name = dict.get('equipmentName')
            equipmentDictionary.update({id : name}) 
        return equipmentDictionary

    def equipmentIdDict(self): 
        equipmentidDictionary = {}
        for dict in self.equipmentList:
            id = dict.get('id')
            name = dict.get('equipmentName')
            equipmentidDictionary.update({name : id}) 
        return equipmentidDictionary
    
    
class conditionList(object):
    def __init__(self):
        self.equipmentList = equipment.objects.values() 

    def conditionDict(self): 
        conditionDictionary = {}
        for dict in self.equipmentList:
            id = dict.get('id')
            name = dict.get('equipmentName')
            conditionDictionary.update({id : name}) 
        return conditionDictionary

    def conditionIdDict(self): 
        conditionidDictionary = {}
        for dict in self.equipmentList:
            id = dict.get('id')
            name = dict.get('equipmentName')
            conditionidDictionary.update({name : id}) 
        return conditionidDictionary