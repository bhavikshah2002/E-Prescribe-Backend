from django.shortcuts import render
from rest_framework import status,generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from main.serializers import *
from accounts.utils import Util
from decouple import config
# Create your views here.

class MedicineView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    def post(self, request,med_name):
        data = {
            "med_name":med_name,
            "med_username":med_name.lower().strip("").replace(" ","")
        }
        serializer = MedicineSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            returnData=serializer.data
            return Response(returnData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,med_name):
        response=self.post(request,med_name)
        if response.status_code==201:
            return render(request,'MedicineAdded.html')
        else:
            return render(request,'MedicineNotAdded.html')

    
class MedicineGetView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineGetSerializer
    def get_queryset(self):
        med=self.request.GET.get('med_name')
        med = med.lower().strip("").replace(" ","") 
        print(med)
        query = Medicine.objects.filter(med_username__icontains = med)
        return query

class MedicineSuggestion(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineGetSerializer
    def post(self, request):
        try:
            doctor = MyUser.objects.get(user_id=self.request.user.user_id)
            med_name = self.request.data["med_name"]
            current_site = 'http://eprescribeserver.pythonanywhere.com'
            relative_link = '/prescription/medicine/'        
            absurl = current_site + relative_link +  med_name
            email_body = 'The Doctor with username ' + doctor.username + 'has suggested to add a medicine.The name of medicine is'+med_name+'\nUse link below to verify the doctor \n' + absurl  
            data_email = {'email_body': email_body, 'to_email': config('EMAIL_HOST_USER'), 'email_subject':f"Add Medicine {med_name}'s suggestion"}     
            Util.send_email(data_email)
            return Response({"success":"Suggestion sent"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"Failure":"Not a valid doctor"}, status=status.HTTP_400_BAD_REQUEST)

class PrescriptionGetUrlDetailsView(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionGetSerializer
    def get(self, request):
        query = Visit.objects.get(url_id = self.request.GET.get('url_id'))
        serializer = VisitUrlSerializer(query)
        returnData={}
        # Add Visit Date
        returnData["visit_date"]=serializer.data["visit_date"]
        returnData["prescription"]=get_prescription(serializer.data["visit_id"])
        session = Session.objects.get(session_id=serializer.data["session"])
        patient = session.patient_id        
        doctor = session.doctor_id
        returnData["doctor"] = {
            "first_name":doctor.first_name,
            "last_name":doctor.last_name,
        }       
        returnData["patient"] = {
            "first_name":patient.first_name,
            "last_name":patient.last_name,
            "age":patient.age
        }       
        return Response(returnData, status=status.HTTP_201_CREATED)

def set_prescription(data):
    serializer = PrescriptionSerializer(data=data)
    try:
        if serializer.is_valid():
            med = Medicine.objects.get(med_id=data['medicine'])
            visit = Visit.objects.get(visit_id = data['visit'])
            serializer.save(medicine = med,visit = visit)
            return serializer.data
        else:
            return serializer.errors
    except:
        return serializer.errors

def get_prescription(id):
    data = Prescription.objects.filter(visit=id)
    serializer = PrescriptionGetSerializer(data,many=True)
    returnData = ""
    returnData= serializer.data
    for i in returnData:
        i['medicine'] = Medicine.objects.get(med_id = i['medicine']).med_name
    return returnData

