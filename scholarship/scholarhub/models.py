from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profiledb(AbstractUser):# csutom can added
    
    
    address=models.CharField(max_length=300,null=True)
    phone=models.IntegerField(null=True)
    is_student=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    profileimg=models.ImageField(upload_to="img/",blank=True)


class Scholarship(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    eligibility=models.TextField()
    amount=models.PositiveIntegerField()
   
    duration=models.CharField(max_length=100)
    deadline=models.DateField()

class StudentApplication(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phone=models.PositiveIntegerField()
    student=models.ForeignKey(Profiledb,on_delete=models.CASCADE,null=True)
    application_date=models.DateField(auto_now=True)
    certificate=models.FileField(upload_to="certificate/",blank=True)
    identity=models.FileField(upload_to="identity/",blank=True)
    photo=models.FileField(upload_to="passsize/",blank=True)

    scholarship=models.ForeignKey(Scholarship,on_delete=models.CASCADE)

    options = (("pending","pending"),("rejected","rejected"),("processing","processing"),("accepted","accepted"))
    status = models.CharField(max_length=30,choices=options,default="pending")







    

