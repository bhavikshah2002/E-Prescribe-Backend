from django.db import models
from accounts.models import MyUser
# Create your models here.

class Session(models.Model):
    session_name=models.CharField(max_length=200,blank=True,default="Comman Disease")
    session_id = models.AutoField(primary_key=True)
    doctor_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,related_name="doctor_id")
    patient_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,related_name="patient_id")
    start_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.session_id)
    