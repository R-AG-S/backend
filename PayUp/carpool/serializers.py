from rest_framework import serializers
from .models import CarPoolRoom

class RoomCreateSerializer(serializers.ModelSerializer):
   class Meta:
        model = CarPoolRoom 
        fields = [              
            "room_name",
            "details",
            "owner"
        ]

    
        