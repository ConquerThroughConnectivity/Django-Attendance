from datetime import datetime
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class AttendanceRecordsModels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    clock_in =models.CharField(max_length=100,blank=True, null=True,default="")
    clock_out =models.CharField(max_length=100,blank=True, null=True,default="")
    date= models.CharField(max_length=100,blank=True, null=True,default="")
    hrs_now =models.CharField(max_length=100,blank=True, null=True,default="")
    total_hrs = models.CharField(max_length=100,blank=True, null=True,default="")
    
    def __str__(self):
        self.clock_in

class ChatModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fromuserid =models.CharField(blank=True, null=True, max_length=100,default="")
    touserid =models.CharField(blank=True, null=True, max_length=100,default="")
    usermessage =models.CharField(blank=True, null=True,max_length=999999,default="")
    isUser =models.BooleanField(blank=True, null=True,max_length=4,default="")
    date_send =models.CharField(blank=True, null=True, max_length=100,default="")
    def __str__(self):
         self.usermessage
    

class Conversation(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     fromuserid=models.CharField(blank=True, null=True, max_length=100,default="")
     userid =models.CharField(blank=True, null=True, max_length=100,default="")
     photo=models.CharField(blank=True, null=True, max_length=100,default="")
     name =models.CharField(blank=True, null=True, max_length=300,default="")
     message =models.JSONField(default=list)
     date_send =models.CharField(blank=True, null=True, max_length=100,default="")

     def __str__(self):
         self.message


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable="")
    name =models.CharField(blank=True, null=True,max_length=100,default="")
    profile_url=models.CharField(blank=True, null=True,max_length=9999,default="")
    password =models.CharField(blank=True, null=True,max_length=100,default="")
    username =models.CharField(blank=True, null=True,unique=True, max_length=100,default="")
    email =models.EmailField(blank=True, null=True, unique=True, max_length=100,default="")
    mobile_number=models.CharField(blank=True, null=True, max_length=100,default="")
    date_joined =models.CharField(blank=True, null=True, max_length=100,default="")
    first_name =models.CharField(blank=True, null=True, max_length=100,default="")
    groups =models.CharField(blank=True, null=True,max_length=100,default="")
    is_active =models.CharField(blank=True, null=True,max_length=100,default="")
    is_staff =models.CharField(blank=True, null=True, max_length=100,default="")
    is_superuser =models.CharField(blank=True, null=True, max_length=100,default="")
    last_login =models.CharField(blank=True, null=True, max_length=100,default="")
    last_name =models.CharField(blank=True, null=True,max_length=100,default="")
    job_title =models.CharField(blank=True, null=True, max_length=100,default="")
    bio =models.CharField(blank=True, null=True, max_length=100,default="")
    user_permissions =models.CharField(blank=True, null=True, max_length=100,default="")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        self.email

class LoginModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email =models.CharField(blank=True, null=True,max_length=100,default="")
    username =models.CharField(blank=True, null=True,max_length=100,default="")
    password =models.CharField(blank=True, null=True,max_length=100,default="")
   
    def __str__(self):
        self.email

class TimeInOutClock(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable="")
   userID =models.CharField(blank=True, null=True,max_length=100,default="")
   time_in =models.CharField(blank=True, null=True,max_length=100,default="")
   time_out =models.CharField(blank=True, null=True,max_length=100,default="")
   hrs = models.CharField(blank=True, null=True, max_length=100,default="")
   time_in_description =models.CharField(blank=True, max_length=100,default="")
   time_out_description =models.CharField(blank=True, null=True,max_length=100,default="")
   time_in_location =models.CharField(blank=True,null=True ,max_length=100, default="")
   time_out_location =models.CharField(blank=True, null=True,max_length=100, default="")
   date =models.CharField(blank=True, null=True, max_length=100,default="")
   def __str__(self):
       self.userID
       
   
