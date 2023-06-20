from django.shortcuts import render
from rest_framework import status,generics
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import *
import random
# Create your views here.

class SessionView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        doctor = MyUser.objects.get(user_id=self.request.user.user_id)
        if serializer.is_valid() and (doctor.is_doctor):
            patient=MyUser.objects.get(user_id=request.data['patient_id'])
            serializer.save(doctor_id=doctor,patient_id=patient,session_name=request.data['session_name'])
            returnData=serializer.data
            return Response(returnData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request,id):
        query = Session.objects.filter(doctor_id = self.request.user.user_id).filter(patient_id=id)
        serializer = SessionSerializer(query, many=True)
        returnData=serializer.data
        for i in returnData:
            i['last_vist']=i['start_date']
            i['num_vist']=random.randint(0,10)
        return Response(returnData, status=status.HTTP_201_CREATED)

    

class PatientDetailsView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    def get(self, request):
        query = Session.objects.filter(doctor_id = self.request.user.user_id)
        serializer = SessionSerializer(query, many=True)
        if not self.request.user.is_doctor:
            return Response({"is_doctor":False}, status=status.HTTP_400_BAD_REQUEST)
        returnData = serializer.data
        patientList=[]
        finalReturn={}
        patient_details=[]
        finalReturn['doctorDetails']=MyUserShortSerializer(self.request.user).data
        for i in returnData:
            if i['patient_id'] not in patientList:
                user_serializer = MyUserShortSerializer(MyUser.objects.get(user_id=i['patient_id']))
                patient_details.append( user_serializer.data)
                patientList.append(i['patient_id'])
        finalReturn['patient_details'] = patient_details    
        return Response(finalReturn)