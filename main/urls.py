from django.urls import path
from .views import *
urlpatterns = [
    path('session/',SessionView.as_view(),name='Session'),
    path('session/<int:id>/',SessionView.as_view(),name='SinglePatientSession'),
    path('patientdetails/',PatientDetailsView.as_view(),name='Patient'),
    path('patientsearch/',PatientSearch.as_view(),name='Search-patient'),
    path('visit/',VisitView.as_view(),name='Visit'),
    path('sessionvisit/',VisitGetView.as_view(),name='Visit-Session'),
]