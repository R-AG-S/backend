from PayUp.firebase import db
from .models import Carpool_Table
from users.models import User_Details_Table

def get_room_details_full(room_id, user_id):
    carpool_ref = db.collection(Carpool_Table).document(room_id)
    if not carpool_ref.get().exists:
        raise Exception("ROOM_DOES_NOT_EXIST")
    carpool_data = carpool_ref.get().to_dict()

    for members in carpool_data['members']:
        if user_id in members:
            return carpool_data
    else:
        raise Exception("FORBIDDEN_USER_NOT_PART_OF_THIS_ROOM")




def get_all_rooms(user_id):

    carpool_ref = db.collection(Carpool_Table)
    query = carpool_ref.where(u'members', u'array_contains', user_id)
    docs = query.get()

    return docs    

def get_all_rooms_details_id(user_id):

    rooms_list = []
    docs = get_all_rooms(user_id)

    for doc in docs:
        rooms_list.append(doc.id)

    return rooms_list

def get_all_rooms_details_full(user_id):

    rooms_list = []
    docs = get_all_rooms(user_id)

    for doc in docs:
        rooms_list.append({"room_id": doc.id, "data": doc.to_dict()})

    return rooms_list

