from django.shortcuts import render
from rest_framework import status,generics
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import *
from rest_framework.authtoken.models import Token
# Create your views here.

class SessionView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        doctor_id = Token.objects.get(key=request.headers['Token']).user_id
        doctor = MyUser.objects.get(user_id=doctor_id)

        if serializer.is_valid():
            patient=MyUser.objects.get(user_id=request.data['patient_id'])
            serializer.save(doctor_id=doctor,patient_id=patient)
            returnData=serializer.data
            return Response(returnData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        doctor_id = Token.objects.get(key=request.headers['Token']).user_id
        query = Session.objects.filter(doctor_id = doctor_id)
        serializer = SessionSerializer(query, many=True)
        return Response(serializer.data)