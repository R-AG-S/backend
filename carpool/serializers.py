from rest_framework import serializers
#from .models import CarPoolRoom

# class RoomCreateSerializer(serializers.ModelSerializer):
#    class Meta:
#         model = CarPoolRoom 
#         fields = [              
#             "room_name",
#             "details",
#             "owner"
#         ]

    

class RoomCreateSerializer(serializers.Serializer):
    room_name = serializers.CharField(max_length=50)
    details = serializers.CharField(max_length=144)
    owner = serializers.CharField(max_length=50)
    petrol_price = serializers.FloatField(min_value=1)
    
class RoomJoinSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=10)