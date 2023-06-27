from django.shortcuts import render
from rest_framework import status,generics
from .models import *
from prescription.models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import *
from prescription.serializers import *
import random
from prescription.views import set_prescription
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

    

class PatientDetailsView(generics.ListAPIView):
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
    
class PatientSearch(generics.ListAPIView):
    queryset=MyUser.objects.all()
    serializer_class=MyUserSerializer
    def get_queryset(self):
        query=self.request.GET.get('patient')           
        allPatient=MyUser.objects.filter(username__icontains=query )
        temp = MyUser.objects.filter(first_name__icontains=query)
        temp2 = MyUser.objects.filter(last_name__icontains=query)
        allPatient= allPatient | temp | temp2 
        allPatient=allPatient.filter(is_doctor = False)
        return allPatient
    
class VisitView(generics.ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    def post(self, request):
        session_detail = self.request.data["sessionDetails"]
        prescription = request.data["prescription"]
        serializer = VisitSerializer(data=session_detail)
        doctor = MyUser.objects.get(user_id=self.request.user.user_id)
        if serializer.is_valid() and (doctor.is_doctor):
            session=Session.objects.get(session_id=session_detail['session']) 
            if session.doctor_id!=doctor:
                return Response({"Error":"Doctor doesn't own this Session"}, status=status.HTTP_400_BAD_REQUEST)             
            serializer.save(session = session)
            returnData=serializer.data
            visit_id = returnData['visit_id']
            returnData['prescription']=[]
            for i in prescription:
                i['visit'] = visit_id
                returnData['prescription'].append(set_prescription(i))
            return Response(returnData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        query = Visit.objects.all()
        serializer = VisitSerializer(query,many = True)
        returnData = ""
        returnData=serializer.data
        return Response(returnData, status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        vis = Visit.objects.get(visit_id = request.data["visit_id"])
        vis.delete()
        return Response("Visit Deleted")
    
class VisitGetView(generics.ListAPIView):
    queryset = Visit.objects.all()
    serializer_class = SessionVisit
    def get(self, request):
        session=self.request.GET.get('session')
        query = Visit.objects.filter(session = session)
        serializer = SessionVisit(query,many = True)
        returnData = ""
        returnData=serializer.data
        return Response(returnData, status=status.HTTP_201_CREATED)
    