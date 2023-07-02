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
from prescription.views import set_prescription,get_prescription
from accounts.views import getDocDetails
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
        query = Session.objects.filter(doctor_id = self.request.user.user_id).filter(patient_id=id).order_by('-start_date')
        serializer = SessionSerializer(query, many=True)
        returnData=serializer.data
        for i in returnData:
            visits = Visit.objects.filter(session = i["session_id"])
            i['last_vist']=i['start_date']
            i['num_visit']=0
            if visits.last()!=None:
                i['last_vist']=visits.last().visit_date
                i['num_visit']=visits.count()
            
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
        session_detail = self.request.data["visitDetails"]
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

def getAllVisitForSession(id):
    query = Visit.objects.filter(session = id).order_by('-visit_date')
    serializer = SessionVisit(query,many = True)
    returnData = ""
    returnData=serializer.data
    # returnData["prescription"]=[]
    for i in returnData:
        i['prescription']=get_prescription(i['visit_id'])
    return returnData

class VisitGetView(generics.ListAPIView):
    queryset = Visit.objects.all()
    serializer_class = SessionVisit
    def get(self, request):
        session=self.request.GET.get('session')
        returnData = getAllVisitForSession(session)
        return Response(returnData, status=status.HTTP_201_CREATED)
    
class PatientGetDoctorView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    def get(self, request):
        query = Session.objects.filter(patient_id = self.request.user.user_id).values_list('doctor_id',flat=True).distinct()
        doctors = DoctorDetails.objects.none()
        for i in query:
            doctors|=DoctorDetails.objects.filter(doctor = i)
        returnData  = getDocDetails(doctors)
        return Response(returnData, status=status.HTTP_201_CREATED)

def addDetailsInSession(returnData):  
    for i in returnData:
        visits = Visit.objects.filter(session = i["session_id"])
        i['last_vist']=i['start_date']
        i['num_visit']=0
        if visits.last()!=None:
            i['last_vist']=visits.last().visit_date
            i['num_visit']=visits.count()
    return returnData 

class PatientGetSessionView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    def get(self, request,id):
        query = Session.objects.filter(patient_id= self.request.user.user_id).filter(doctor_id=id).order_by('-start_date')
        serializer = SessionSerializer(query, many=True)
        returnData=serializer.data
        returnData = addDetailsInSession(returnData)    
        return Response(returnData, status=status.HTTP_201_CREATED)
    
class PatientGetRecentSessionView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    def get(self, request):
        query = Session.objects.filter(patient_id= self.request.user.user_id).order_by('-start_date')
        serializer = SessionSerializer(query, many=True)
        returnData=serializer.data
        returnData = addDetailsInSession(returnData)   
        return Response(returnData, status=status.HTTP_201_CREATED)
            
class PatientGetRecentVisitView(generics.ListAPIView):
    queryset = Visit.objects.all()
    serializer_class = SessionVisit
    def get(self, request):
        sessions = Session.objects.filter(patient_id=self.request.user.user_id).values("session_id")
        session_id_list = []
        for i in sessions:
            session_id_list.append(i['session_id'])

        query = Visit.objects.filter(session__in= session_id_list).order_by('-visit_date')
        serializer = SessionVisit(query,many = True)
        returnData = ""
        returnData=serializer.data
        # returnData["prescription"]=[]
        for i in returnData:
            i['prescription']=get_prescription(i['visit_id'])
        return Response(returnData, status=status.HTTP_201_CREATED)

class SessionByIDView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    def get(self, request):
        query = Session.objects.filter(session_id= self.request.GET.get('session_id')).order_by('-start_date')
        serializer = SessionSerializer(query, many=True)
        returnData=serializer.data
        returnData = addDetailsInSession(returnData)    
        return Response(returnData, status=status.HTTP_201_CREATED)
