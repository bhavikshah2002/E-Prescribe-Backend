from django.urls import path
from .views import *
urlpatterns = [
    path('register/',Registration.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('email_verify/',verifyEmail,name='verifyEmail'),
    path('doctor_verify/',verifyDoctor,name='verifyDoctor'),
    path('MyUser/<int:pk>/',MyUserView.as_view(),name='MyUser'),
    path('doctordetails/',DoctorDetailsView.as_view(),name='DoctorDetails'),
    path('doctordetails/update/',DoctorDetailsUpdateView.as_view(),name='DoctorDetailsUpdate'),
]