from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .utils import Util
from .models import *
from django.urls import reverse
from rest_framework.decorators import api_view
from django.contrib.auth.models import update_last_login
from django.shortcuts import render
from decouple import config
# Create your views here.
class Registration(generics.CreateAPIView):
    serializer_class=RegistrationSerializer
    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            serializer = RegistrationSerializer(data = request.data)
            data={}
            if serializer.is_valid():
                my_user = serializer.save()
                token = Token.objects.get(user = my_user).key
                token = Token.objects.get(user = my_user).key
                data['old_token']=token
                data['username']=my_user.username
                current_site = 'http://eprescribeserver.pythonanywhere.com'
                relative_link = reverse('verifyEmail')          
                absurl = current_site + relative_link + "?token="+str(token) 
                email_body = 'Hi ' + my_user.username + ' Use link below to verify your email \n' + absurl  
                data_email = {'email_body': email_body, 'to_email': my_user.email, 'email_subject':'Verify your email'}     
                Util.send_email(data_email)
                if my_user.is_doctor == True:
                    relative_link2 = reverse('verifyDoctor')          
                    absurl = current_site + relative_link2 + "?user_id="+str(my_user.user_id) 
                    email_body = 'Please Verify ' + my_user.username + 'as a valid doctor.\nUse link below to verify the doctor \n' + absurl  
                    data_email = {'email_body': email_body, 'to_email': config('EMAIL_HOST_USER'), 'email_subject':f'Verify the doctor with username {my_user.username}'}     
                    Util.send_email(data_email)

            else:
                data=serializer.errors
            return Response(data)


@api_view(['GET'])
def verifyEmail(request): 
    data = {}
    token = request.GET.get('token')
    try:
        user = MyUser.objects.get(auth_token = token)
    except:
        content = {'detail': 'User already activated!'}
        return render(request, 'AlreadyEmailVerified.html')
    token = request.GET.get('token')
    if user.is_active == False:
        user.is_active = True
        user.save()
        Token.objects.get(user = user).delete()
        Token.objects.create(user = user)
        new_token = Token.objects.get(user = user).key       
        return render(request, 'EmailVerify.html')
    else:
        data={'status':'Email Not Verified'}
        return render(request, 'EmailNotVerified.html')
    
@api_view(['GET'])
def verifyDoctor(request): 
    data = {}
    user_id = request.GET.get('user_id')
    try:
        user = MyUser.objects.get(user_id = user_id)
    except:
        content = {'detail': 'User already activated!'}
        return render(request, 'NoUserFound.html')
    if user.is_verified == False:
        user.is_verified = True
        user.save()    
        return render(request, 'DoctorVerified.html')
    else:
        data={'status':'Doctor Not Verified'}
        return render(request, 'NoUserFound.html')

class LoginView(generics.CreateAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        if request.method == 'POST':
            serializer = LoginSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)
            user = MyUser.objects.get(email = serializer.data['email'])
            token = Token.objects.get(user = user).key
            update_last_login(None, user) #update last login
            if user.is_doctor==True and user.is_verified==False:
                return Response({'email':user.email,"is_doctor":user.is_doctor,"is_verified":user.is_verified}, status = status.HTTP_401_UNAUTHORIZED)
            data = {}
            data['token'] = token
            data['user_id']=user.user_id
            data['username']=user.username
            data['is_doctor']=user.is_doctor
            return Response(data, status = status.HTTP_200_OK)

class MyUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    def get(self,request,pk):
        query=MyUser.objects.get(pk=pk)        
        serializer=MyUserSerializer(query)       
        return Response(serializer.data)
    def patch(self, request,pk):
        query=MyUser.objects.get(pk=pk) 
        serializer = MyUserSerializer(query, data=request.data,partial=True)            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class DoctorDetailsView(generics.ListCreateAPIView):
    queryset = DoctorDetails.objects.all()
    serializer_class = DoctorDetailsSerializer
    def post(self, request):
        serializer = DoctorDetailsSerializer(data=request.data)
        doctor = MyUser.objects.get(user_id=request.data["doctor"])
        if serializer.is_valid() :
            serializer.save(doctor=doctor)
            returnData=serializer.data
            return Response(returnData, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        query = DoctorDetails.objects.all()
        serializer = DoctorDetailsSerializer(query, many=True)
        returnData=serializer.data
        return Response(returnData, status=status.HTTP_201_CREATED)