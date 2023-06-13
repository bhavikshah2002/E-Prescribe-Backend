from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.urls import reverse
from django.contrib.auth.models import update_last_login
from django.shortcuts import render
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
                data['token']=token
                data['username']=my_user.username
                # current_site = 'http://gitbase.sytes.net:8081'
                # relative_link = reverse('verifyEmail')          
                # absurl = current_site + relative_link + "?token="+str(token) 
                # email_body = 'Hi ' + my_user.username + ' Use link below to verify your email \n' + absurl  
                # data_email = {'email_body': email_body, 'to_email': my_user.email, 'email_subject':'Verify your email'}     
                # Util.send_email(data_email)           
            else:
                data=serializer.errors
            return Response(data)

# def verifyEmail(request): 
#     data = {}
#     token = request.GET.get('token')
#     try:
#         user = MyUser.objects.get(auth_token = token)
#     except:
#         content = {'detail': 'User already activated!'}
#         return render(request, 'AlreadyEmailVerified.html')
#     token = request.GET.get('token')
#     if user.is_active == False:
#         user.is_active = True
#         user.save()
#         Token.objects.get(user = user).delete()
#         Token.objects.create(user = user)
#         new_token = Token.objects.get(user = user).key       
#         return render(request, 'EmailVerify.html')
#     else:
#         data={'status':'Email Not Verified'}
#         return render(request, 'EmailNotVerified.html')

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
            data['email'] = user.email
            data['token'] = token
            data['user_id']=user.user_id
            data['username']=user.username
            return Response(data, status = status.HTTP_200_OK)

class MyUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    def get(self,request,pk):
        query=MyUser.objects.filter(user_id=self.request.user.user_id).get(pk=pk)   
        print(query)     
        serializer=MyUserSerializer(query)       
        return Response(serializer.data)
    def patch(self, request,pk):
        query = MyUser.objects.filter(user_id=self.request.user.user_id).get(pk=pk)
        serializer = MyUserSerializer(query, data=request.data,partial=True)            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
