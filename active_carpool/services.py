from carpool.models import Carpool_Table
from django.utils import timezone
from PayUp.firebase import GeoPoint, db

from .models import ACTIVE_CARPOOL_TABLE, INACTIVE_SESSIONS_TABLE, init_inactive_table
from .serializers import active_session_parser
from .cost_function import cost_function_linear_version1


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


def get_history_if_room_valid(room_id, user_id, active_check=False, must_exist=False):
    carpool_ref = db.collection(Carpool_Table).document(room_id).get()
    if not carpool_ref.exists:
        raise Exception("ROOM_DOES_NOT_EXIST")
    if user_id not in carpool_ref.to_dict()['members']:
        raise Exception("FORBIDDEN_USER_NOT_PART_OF_THE_ROOM")

    history_ref = db.collection(INACTIVE_SESSIONS_TABLE).document(room_id)
    if active_check and history_ref.get().exists:
        raise Exception("ROOM_ALREADY_HAS_HISTORY") 
    if must_exist and not(history_ref.get().exists):
        raise Exception("ROOM_DOES_NOT_HAVE_HISTORY")  

    return history_ref


def start_active_session(data, user_id):
    

    room_id = data['room_id']
    lat = data['lat']
    lng = data['lng']
    car = data['car']
    mileage = data['mileage']

    active_room_ref = get_active_room_if_room_valid(room_id, user_id, active_check=True)

    start_time = timezone.now() 
    set_data = {

    'driver': user_id,
    'initial_coordinates': GeoPoint(lat, lng),
    'car': car,
    'mileage': mileage,
    'start_time': start_time,
    'passengers_in_car': [],
    'dropped_of_passengers': [],

    'passenger_pickup_details': [],
    'passenger_dropoff_details': [],

    }
    active_room_ref.set(set_data)

    #active_session_start_notification(room_id, user_id)

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
    #try:
        #active_session_join_notification(session_data)

    return {"SUCCESS": "ACTIVE_SESSION_JOINED", "SESSION_DETAILS": active_session_parser(session_data)}



def leave_active_session(data, user_id):
    
    room_id = data['room_id']
    lat = data['lat']
    lng = data['lng']
    distance = data['distance']

    active_room_ref = get_active_room_if_room_valid(room_id, user_id, must_exist=True)
    
    session_data = active_room_ref.get().to_dict()
    if user_id not in session_data['passengers_in_car']:
        raise Exception("USER_IS_NOT_PART_OF_SESSION")
    leave_time = timezone.now() 
    pickup_data = {
        user_id:
            {
                'coordinates': GeoPoint(lat, lng),
                'time': leave_time,
                'distance': distance
            }   
    }

    session_data['passenger_dropoff_details'].append(pickup_data)
    session_data['passengers_in_car'].remove(user_id)
    session_data['dropped_of_passengers'].append(user_id)

    active_room_ref.set(session_data)

    #active_session_join_notification(session_data)

    return {"SUCCESS": "ACTIVE_SESSION_LEFT", "SESSION_DETAILS": active_session_parser(session_data)}
    

    

def end_active_session(data, user_id):
    
    room_id = data['room_id']
    lat = data['lat']
    lng = data['lng']
    distance = data['distance']
    wear_and_tear_factor = data['wear_and_tear_factor']
    driver_discount= data['driver_discount']

    debug = data['debug']
    

    active_room_ref = get_active_room_if_room_valid(room_id, user_id, must_exist=True)
    end_time = timezone.now() 
    session_data = active_room_ref.get().to_dict()

    if user_id in session_data['driver']:

        inactive_ref = db.collection(INACTIVE_SESSIONS_TABLE).document(room_id)
        session_data['end_time'] = end_time
        session_data['distance'] = distance
        session_data['final_coordinates'] = GeoPoint(lat, lng)
        session_data['participants_list'] = (session_data['passengers_in_car'] 
                    + session_data['dropped_of_passengers'] + [session_data['driver']])
        
        session_data['cost_split'] = []

        # Cleaning up data.
        for passenger in session_data['passengers_in_car']:
            session_data['passenger_dropoff_details'].append({
                    passenger:{
                            'coordinates': GeoPoint(lat, lng),
                            'time': end_time,
                            'distance': distance
                        } 
            })
       

        session_data.pop('passengers_in_car')
        session_data.pop('dropped_of_passengers')
        # End Cleaning up data.
        if inactive_ref.get().exists:
            inactive_session = inactive_ref.get().to_dict()
        else: 
            inactive_session = init_inactive_table()




        

      
        #active_session_end_notification(session_data)
        parsed_data = active_session_parser(session_data)
    
        # TODO:
        # active_session_end_notification(parsed_data)
        room_fuel_cost = db.collection(Carpool_Table).document(room_id).get().to_dict()['petrol_price']
        
        parsed_data = cost_function_linear_version1(parsed_data, room_fuel_cost, wear_and_tear_factor, driver_discount)
        if not debug:
            active_room_ref.delete()    # Delete Active Session
            inactive_session['session_count'] = str(int(inactive_session['session_count']) + 1)
            inactive_session['history'].append(parsed_data)
            inactive_session['last_session'] = end_time
            #add_to_cost_split_global(parsed_data['cost_split'])
            inactive_ref.set(inactive_session)

        return {"SUCCESS": "ACTIVE_SESSION_ENDED", "SESSION_DETAILS": parsed_data}
    
    else:
        raise Exception("FORBIDDEN_ONLY_DRIVER_CAN_END_SESSION")
