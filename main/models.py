from django.db import models
from accounts.models import MyUser
import uuid
# Create your models here.

class Session(models.Model):
    session_name=models.CharField(max_length=200,blank=True,default="Comman Disease")
    session_id = models.AutoField(primary_key=True)
    doctor_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,related_name="doctor_id")
    patient_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,related_name="patient_id")
    start_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.session_id)

class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    url_id = models.UUIDField(default = uuid.uuid4)
    session = models.ForeignKey(Session, on_delete=models.CASCADE,null=True,related_name="session")
    visit_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField(max_length=250,blank=True,null=True)
    note = models.TextField(max_length=500,blank=True,null=True)
    temperature = models.DecimalField(null=True,blank=True,max_digits=5,decimal_places=2)
    sugar = models.IntegerField(null=True,blank=True)
    bp = models.CharField(null=True,blank=True,max_length=10)
    def __str__(self):
        return str(self.visit_id)