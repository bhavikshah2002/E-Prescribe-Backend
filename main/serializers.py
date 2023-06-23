from rest_framework import serializers
from .models import *

class SessionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Session
        fields="__all__"

class VisitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Visit
        fields="__all__"

