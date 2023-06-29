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

class MedicineSuggestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Medicine
        fields=['med_name']

class PrescriptionSerializer(serializers.ModelSerializer):    
    class Meta:
        model=Prescription
        fields="__all__"

class PrescriptionGetSerializer(serializers.ModelSerializer):    
    class Meta:
        model=Prescription
        fields=['pres_id','medicine','morning','afternoon','night','num_days']