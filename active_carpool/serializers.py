from rest_framework import serializers
from Payup.general_values import ROOM_ID_LENGTH
    

class StartActiveSessionSerializer(serializers.Serializer):

    room_id = serializers.CharField(max_length=ROOM_ID_LENGTH)
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    car = serializers.CharField(max_length=200)

    


