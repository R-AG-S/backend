#from .models import CarPoolRoom


# def createroom(validated_data):
#     try:
#         room = CarPoolRoom.objects.create(**validated_data)
#         return room.pk
#     except Exception as e:
#         raise e  
from PayUp.firebase import db, unique_key_generator
from datetime import datetime
from users.services import initialise_user_table


def add_room_to_user_data_table(room_id, user_id):
    try:
        time = datetime.now()  
        user_ref = db.collection("User-Details").document(room_id)

        if not user_ref.get().exists:
            user_ref = initialise_user_table(room_id)

        user_table = user_ref.get().to_dict()
        room_data = {"name": user_id, "joined_on": time}
        user_table["rooms"].append(room_data)

        user_ref.set(user_table)
        return user_ref
    except Exception as e:
        return e



def createroom(validated_data, user_id):
    try:
        id = unique_key_generator(6)
        carpool_ref = db.collection('CP_ROOM').document(id)
        while carpool_ref.get().exists:       # In the off chance that the key already exists, generate new key.
            print("Damn Danial Duplicate: ", id)
            id = unique_key_generator(6)
            carpool_ref = db.collection('CP_ROOM').document(id)
            

        time = datetime.now()
        room_name = validated_data['room_name']
        details = validated_data['details']
        owner = user_id
        petrol_price = validated_data['petrol_price']
        members = [{"name": owner, "joined_on": time}]
    
        data = {
            "room_name": room_name,
            "details": details,
            "owner": owner,
            "petrol_price": petrol_price,
            "members": members,
            "created_on": time
        }
        carpool_ref.set(data)

        add_room_to_user_data_table(carpool_ref.id, user_id)

        return carpool_ref.id

    except Exception as e:
        return e




def joinroom(room_id: str, user_id: str):

    try:

        carpool_ref = db.collection('CP_ROOM').document(room_id)
        if not carpool_ref.get().exists:
            raise Exception("ROOM_DOES_NOT_EXIST")

        time = datetime.now()    
        member_add_data = {"name": user_id, "joined_on": time}

        carpool_data = carpool_ref.get().to_dict()
        carpool_data['members'].append(member_add_data)

        carpool_ref.set(carpool_data)

        add_room_to_user_data_table(room_id, user_id)

        return "ROOM_JOINED"

    except Exception as e:
        return e