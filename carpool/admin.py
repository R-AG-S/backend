from django.contrib import admin
from .models import CarPoolRoom

# Register your models here.

class CarPoolRoomModelAdmin(admin.ModelAdmin):
	list_display = ["room_id", "room_name", "owner"]           
	
	class Meta:                     
		model = CarPoolRoom

admin.site.register(CarPoolRoom, CarPoolRoomModelAdmin) 