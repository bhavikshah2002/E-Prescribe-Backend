from django.urls import path
from .views import *
urlpatterns = [
    path('session/',SessionView.as_view(),name='Session'),
    path('session/<int:id>/',SessionView.as_view(),name='SinglePatientSession'),
    path('patientdetails/',PatientDetailsView.as_view(),name='Doctor-Patient'),
    path('patientsearch/',PatientSearch.as_view(),name='Search-patient'),
    path('visit/',VisitView.as_view(),name='Visit'),
    path('sessionvisit/',VisitGetView.as_view(),name='Visit-Session'),
    path('patientgetdoctor/',PatientGetDoctorView.as_view(),name='PatientGetDoctor'),
    path('patientgetsession/<int:id>/',PatientGetSessionView.as_view(),name='PatientGetSession'),
    path('patientgetrecentvisit/',PatientGetRecentVisitView.as_view(),name='PatientGetRecentVisit'),
    path('patientgetrecentsession/',PatientGetRecentSessionView.as_view(),name='PatientGetRecentSession'),  
    path('sessionbyid/',SessionByIDView.as_view(),name='SessionByID'),  
]