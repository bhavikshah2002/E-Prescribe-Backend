from django.db import models
from main.models import *
# Create your models here.
class Medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    med_name = models.TextField()
    med_username = models.TextField(unique=True,blank=False,default="medicine")
    REQUIRED_FIELDS=['med_username']
    def __str__(self):
        return str(self.med_id)

class Prescription(models.Model):
    pres_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE,null=True,related_name="visit")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE,null=True,related_name="medicine")
    morning = models.IntegerField(null=True,blank=True,default=0)
    afternoon = models.IntegerField(null=True,blank=True,default=0)
    night = models.IntegerField(null=True,blank=True,default=0)
    num_days = models.IntegerField(null=True,blank=True,default=1)
    def __str__(self):
        return str(self.pres_id)
