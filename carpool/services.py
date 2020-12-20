from PayUp.firebase import db, unique_key_generator
from django.utils import timezone
from users.services import initialise_user_table
from .models import Carpool_Table, Free_User_Create_Room_Limit
from active_carpool.models import INACTIVE_SESSIONS_TABLE, init_inactive_table

def add_room_to_user_data_table(room_id, user_id, created=False):
    try:
        time = timezone.now()  
        user_ref = db.collection("User-Details").document(user_id)

        if not user_ref.get().exists:
            user_ref = initialise_user_table(user_id)

        user_table = user_ref.get().to_dict()

        if created:
            if len(user_table['rooms_created']) > Free_User_Create_Room_Limit:
                return None      # Limit Reached 

        #room_data = {"room_id": room_id, "joined_on": time}
        room_data = room_id
        user_table["rooms"].append(room_data)
        if created:
            user_table["rooms_created"].append(room_data)
            

        user_ref.set(user_table)
        return user_ref
    except Exception as e:
        raise e



def createroom(validated_data, user_id):
    try:

        id = unique_key_generator(6)
        carpool_ref = db.collection(Carpool_Table).document(id)
        while carpool_ref.get().exists:       # In the off chance that the key already exists, generate new key.
            print("Damn Danial Duplicate: ", id)
            id = unique_key_generator(6)
            carpool_ref = db.collection(Carpool_Table).document(id)
            
        if add_room_to_user_data_table(room_id= carpool_ref.id, user_id = user_id, created= True):
        # Add to User Details. Check if User's Room Limit has exceeded. 
            
            time = timezone.now()
            room_name = validated_data['room_name']
            details = validated_data['details']
            member = user_id
            petrol_price = validated_data['petrol_price']
            #members = [ {"user_id": member, "joined_on": time}  ]
            members = [ member ] 
            
            data = {
                "room_name": room_name,
                "details": details,
                "owner": member,
                "petrol_price": petrol_price,
                "members": members,
                "created_on": time
            }
            carpool_ref.set(data)

            inactive_table = db.collection(INACTIVE_SESSIONS_TABLE).document(carpool_ref.id)
            inactive_init_data = init_inactive_table()

            return {"ROOM_ID": carpool_ref.id, "DATA": data} 
        else:
            return {"ERROR": "USER_ROOM_CREATE_LIMIT_REACHED", 
                    "MESSAGE": "Sorry, the room limit for your account has been reached."}

    except Exception as e:
        raise e




def joinroom(room_id: str, user_id: str):

    try:

        carpool_ref = db.collection(Carpool_Table).document(room_id)
        if not carpool_ref.get().exists:
            raise Exception("ROOM_DOES_NOT_EXIST")

        time = timezone.now()    
        #member_add_data = {"user_id": user_id, "joined_on": time}
        member_add_data = user_id

        carpool_data = carpool_ref.get().to_dict()
        for members in carpool_data['members']:
            if user_id in members:
                raise Exception("USER_ALREADY_PART_OF_ROOM")

        else:
                carpool_data['members'].append(member_add_data)
                carpool_ref.set(carpool_data)
                add_room_to_user_data_table(room_id, user_id)
                return carpool_data

    except Exception as e:
        raise e



