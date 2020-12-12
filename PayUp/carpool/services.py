from .models import CarPoolRoom


def createroom(validated_data):
    try:
        room = CarPoolRoom.objects.create(**validated_data)
        return room.pk
    except Exception as e:
        raise e  
