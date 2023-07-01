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

class SessionVisit(serializers.ModelSerializer):
    class Meta:
        model=Visit
        fields="__all__"

class VisitUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model=Visit
        fields=["visit_id","session","visit_date"]

