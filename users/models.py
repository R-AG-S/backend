
from django.db import models
from django.contrib.auth.models import AbstractUser
from carpool.models import CarPoolRoom 

#Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    rooms = models.ManyToManyField(CarPoolRoom)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering=["-timestamp", "-updated"]

  
