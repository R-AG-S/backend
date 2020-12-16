from PayUp.firebase import db
from .models import Carpool_Table

def get_room_details_full(room_id, user_id):
    carpool_ref = db.collection(Carpool_Table).document(room_id)
    if not carpool_ref.get().exists:
        raise Exception("ROOM_DOES_NOT_EXIST")
    carpool_data = carpool_ref.get().to_dict()

    for members in carpool_data['members']:
        if user_id in members['user_id']:
            return carpool_data
    else:
        raise Exception("FORBIDDEN_USER_NOT_PART_OF_THIS_ROOM")