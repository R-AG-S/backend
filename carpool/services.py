#from .models import CarPoolRoom


# def createroom(validated_data):
#     try:
#         room = CarPoolRoom.objects.create(**validated_data)
#         return room.pk
#     except Exception as e:
#         raise e  
from PayUp.firebase import db, unique_key_generator


def createroom(validated_data):
    try:
        id = unique_key_generator(6)
        carpool_ref = db.collection('CP_ROOM').document(id)
        while carpool_ref.get().exists:       # In the off chance that the key already exists, generate new key.
            print("Damn Danial", id)
            key = unique_key_generator(6)
            carpool_ref = db.collection('CP_ROOM').document(id)
            

    
        room_name = validated_data['room_name']
        details = validated_data['details']
        owner = validated_data['owner']
        petrol_price = validated_data['petrol_price']
    
        data = {
            "room_name": room_name,
            "details": details,
            "owner": owner,
            "petrol_price": petrol_price
        }
        carpool_ref.set(data)

        return carpool_ref.id

    except Exception as e:
        return e