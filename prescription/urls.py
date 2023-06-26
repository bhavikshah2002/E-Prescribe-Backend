from django.urls import path
from .views import *
urlpatterns = [
    path('medicine/<str:med_name>/',MedicineView.as_view(),name='Medicine'),
    path('medicine/',MedicineGetView.as_view(),name='MedicineGet'),
]