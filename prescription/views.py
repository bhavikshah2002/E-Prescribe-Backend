from django.shortcuts import render
from rest_framework import status,generics
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from main.serializers import *
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
            render(request, 'MedicineAdded.html')
        else:
            render(request, 'MedicineNotAdded.html')
        return response

    
class MedicineGetView(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineGetSerializer
    def get(self, request):
        query = Medicine.objects.all()
        serializer = MedicineGetSerializer(query,many = True)
        # returnData = ""
        returnData=serializer.data
        return Response(returnData, status=status.HTTP_201_CREATED)
    
    
