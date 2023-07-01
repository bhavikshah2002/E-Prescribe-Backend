from django.urls import path
from .views import *
urlpatterns = [
    path('medicine/<str:med_name>/',MedicineView.as_view(),name='Medicine'),
    path('medicinesearch/',MedicineGetView.as_view(),name='MedicineGet'),
    path('medicinesuggest/',MedicineSuggestion.as_view(),name='MedicineSuggest'),
    path('geturldetails/',PrescriptionGetUrlDetailsView.as_view(),name='PrescriptionGetUrlDetails'),
]