from rest_framework import serializers
#from .models import CarPoolRoom

class RoomCreateSerializer(serializers.Serializer):
    room_name = serializers.CharField(max_length=50)
    details = serializers.CharField(max_length=144)
    petrol_price = serializers.FloatField(min_value=0)
    
class RoomIDSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=10)