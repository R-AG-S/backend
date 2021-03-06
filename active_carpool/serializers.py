from copy import copy

from PayUp.general_values import ROOM_ID_LENGTH
from rest_framework import serializers


class CreateActiveSessionSerializer(serializers.Serializer):

    room_id = serializers.CharField(max_length=ROOM_ID_LENGTH)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    car = serializers.CharField(max_length=100)
    mileage = serializers.FloatField(required=False, default = 15)


class StartActiveSessionSerializer(serializers.Serializer):

    room_id = serializers.CharField(max_length=ROOM_ID_LENGTH)
    lat = serializers.FloatField()
    lng = serializers.FloatField()

class LeaveActiveSessionSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=ROOM_ID_LENGTH)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    distance = serializers.FloatField(required=False, default = 0)


class EndSessionSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=ROOM_ID_LENGTH)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    distance = serializers.FloatField()
    
    wear_and_tear_factor = serializers.FloatField(required=False, default=0.2)
    driver_discount = serializers.FloatField(required=False, default=0.05)

    cancel_session = serializers.BooleanField(required=False, default=False)
    debug = serializers.BooleanField(default=False, required=False)

class TestSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=ROOM_ID_LENGTH)

    

def detail_parser(detail_list):
    data = []
    for item in detail_list:
        itemkey = list(item.keys())[0]
        itemvalue = list(item.values())[0]
        if 'distance' in itemvalue:
            data.append({
                itemkey: {
                    'coordinates': [
                            itemvalue['coordinates'].latitude,
                            itemvalue['coordinates'].longitude
                        ],
                    'time': itemvalue['time'],
                    'distance': itemvalue['distance']
                }
            })
        else:
            data.append({
                itemkey: {
                    'coordinates': [
                            itemvalue['coordinates'].latitude,
                            itemvalue['coordinates'].longitude
                        ],
                    'time': itemvalue['time']
                }
            })
    return data


def active_session_parser(session_data):     
    parsed_data = copy(session_data)
    parsed_data['passenger_dropoff_details'] = []
    parsed_data['passenger_pickup_details'] = []
    parsed_data['initial_coordinates'] = []
    try:
        

        if 'final_coordinates' in session_data:
            parsed_data['final_coordinates'] = [
                session_data['final_coordinates'].latitude,
                session_data['final_coordinates'].longitude,
            ]
        if 'passenger_dropoff_details' in session_data:
            parsed_data['initial_coordinates'] = [
                session_data['initial_coordinates'].latitude,
                session_data['initial_coordinates'].longitude
            ]
        if 'passenger_dropoff_details' in parsed_data:
            parsed_data['passenger_dropoff_details'] = detail_parser(session_data['passenger_dropoff_details'])
        if 'passenger_pickup_details' in parsed_data:
            parsed_data['passenger_pickup_details'] = detail_parser(session_data['passenger_pickup_details'])


    except Exception as e:
        print("ERROR " + str(e))
        
    return parsed_data
