from PayUp.firebase import db, GeoPoint
from .models import ACTIVE_CARPOOL_TABLE
from carpool.models import Carpool_Table
from django.utils import timezone
from .serializers import active_session_parser

def get_active_room_if_room_valid(room_id, user_id, active_check=False, must_exist=False):
    carpool_ref = db.collection(Carpool_Table).document(room_id).get()
    if not carpool_ref.exists:
        raise Exception("ROOM_DOES_NOT_EXIST")
    if user_id not in carpool_ref.to_dict()['members']:
        raise Exception("FORBIDDEN_USER_NOT_PART_OF_THE_ROOM")

    active_room_ref = db.collection(ACTIVE_CARPOOL_TABLE).document(room_id)
    if active_check and active_room_ref.get().exists:
        raise Exception("ROOM_ALREADY_HAS_ACTIVE_SESSION") 
    if must_exist and not(active_room_ref.get().exists):
        raise Exception("ROOM_DOES_NOT_HAVE_ACTIVE_SESSION")  

    return active_room_ref



def start_active_session(data, user_id):
    

    room_id = data['room_id']
    lat = data['lat']
    lng = data['lng']
    car = data['car']
    active_room_ref = get_active_room_if_room_valid(room_id, user_id, active_check=True)
    start_time = timezone.now() 
    set_data = {

    'driver': user_id,
    'initial_coordinates': GeoPoint(lat, lng),
    'car': car,
    'start_time': start_time,
    'passengers_in_car': [],
    'dropped_of_passengers': [],

    'passenger_pickup_details': [],
    'passenger_dropoff_details': [],

    }
    active_room_ref.set(set_data)

    #active_session_start_notification(session_data)

    return {"SUCCESS": "ACTIVE_SESSION_STARTED"}



def join_active_session(data, user_id):
    

    room_id = data['room_id']
    lat = data['lat']
    lng = data['lng']

    active_room_ref = get_active_room_if_room_valid(room_id, user_id, must_exist=True)
    
    session_data = active_room_ref.get().to_dict()
    if user_id in session_data['passengers_in_car'] or user_id in session_data['driver'] :
        raise Exception("USER_ALREADY_JOINED_ACTIVE_SESSION")

    join_time = timezone.now() 
    pickup_data = {
        user_id:
            {
                'coordinates': GeoPoint(lat, lng),
                'time': join_time
            }   
    }

    session_data['passenger_pickup_details'].append(pickup_data)
    session_data['passengers_in_car'].append(user_id)


    active_room_ref.set(session_data)

    #active_session_join_notification(session_data)

    return {"SUCCESS": "ACTIVE_SESSION_JOINED", "SESSION_DETAILS": active_session_parser(session_data)}




    

    

