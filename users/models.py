from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

#Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    full_name = models.CharField(max_length=100, default="")
    phone_number = PhoneNumberField()
    email = models.EmailField()
    primary_address = models.CharField(max_length=500, default='')
    

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    class Meta:
        ordering=["-timestamp", "-updated"]
