from rest_framework import serializers
from .models import *

class MedicineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Medicine
        fields="__all__"

class MedicineGetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Medicine
        fields=['med_id','med_name']
