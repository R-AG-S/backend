  
from django.db import models
import secrets

# Create your models here.

def get_code():
  return secrets.token_hex(3).upper()

class CarPoolRoom(models.Model):
    room_id = models.CharField(max_length=6, primary_key=True, default=get_code, editable=False)
    room_name = models.CharField(max_length=120, unique=True)
    details = models.TextField()
    owner = models.CharField(max_length=50)
    members = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering=["-timestamp","-updated"]
    
    def __str__(self):
        return self.room_id


     