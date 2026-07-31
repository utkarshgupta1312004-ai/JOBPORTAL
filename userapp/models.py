from django.db import models
from adminapp.models import JobInfo
from mainapp.models import JobSeeker

# Create your models here.
class Response(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    contactno=models.CharField(max_length=15)
    responsetype=models.CharField(max_length=50)
    subject=models.CharField(max_length=500)
    responsetext=models.CharField(max_length=2000)
    posteddate=models.CharField(max_length=30)

class AppliedJob(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(JobInfo, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applieddate = models.CharField(max_length=30)
    status = models.CharField(max_length=50, default='Request Pending')

