# Author: Tharine Ramachandran
# Data Written: 10/08/2020
from django.forms import ModelForm
from django import forms 
from SafetyManagerApp.models import equipment
from django.forms import ModelForm

ppeequipmentlist = equipment.objects.all().values_list("id", "id")

class ImageUploadForm(forms.Form):
        image = forms.CharField()
        objectsDetected =forms.MultipleChoiceField(choices = ppeequipmentlist ,required=False)
        objectsViolated = forms.MultipleChoiceField(choices = ppeequipmentlist ,required=False )
        top = forms.CharField( required=True) 
        left =forms.CharField( required=True) 
        width =forms.CharField( required=True) 
        height =forms.CharField( required=True)

        # Lina added
        countcheck = forms.CharField(required=True)
        # end of Lina added 

class DetectionUploadForm(forms.Form):
        image = forms.CharField() 
        top = forms.CharField( required=True) 
        left =forms.CharField( required=True) 
        width =forms.CharField( required=True) 
        height =forms.CharField( required=True) 
        itemDetectionList=forms.MultipleChoiceField(choices = ppeequipmentlist ,required=False)
        checkForObjects=   forms.BooleanField( required=False) 

class EquipmentForm(forms.Form): 
        equipmentName = forms.CharField()
        equipmentIcon = forms.CharField()

class EquipmentUpdateForm(forms.Form): 
        equipmentName = forms.CharField()
        equipmentIcon = forms.CharField()
        id = forms.CharField()

class AccessTokenForm(forms.Form): 
        tokenStr = forms.CharField()
        isValid = forms.BooleanField( required=False)

class AccessTokenUpdateForm(forms.Form): 
        tokenStr = forms.CharField(required=False)
        id = forms.CharField()
        isValid = forms.NullBooleanField( required=False)

class PPESelectionForm(forms.Form): 
        selectionEquipment = forms.MultipleChoiceField(choices = ppeequipmentlist ,required=True )

class ChannelsForm(forms.Form): 
        channelStr = forms.CharField()
        tokenStr = forms.CharField()
        isValid = forms.BooleanField( ) 

class LogDeleteForm(forms.Form): 
        id = forms.CharField()   
         
class sendMessageForm(forms.Form): 
        text = forms.CharField()
        
class ChannelsUpdateForm(forms.Form): 
        channelStr = forms.CharField( empty_value = 'None')
        isValid = forms.NullBooleanField( required=False)
        tokenStr = forms.CharField( empty_value = 'None')
        id = forms.CharField()

class TestForm(forms.Form):
        image = forms.CharField()
        ObjectViolated = forms.CharField()
        condition = forms.CharField()
        
