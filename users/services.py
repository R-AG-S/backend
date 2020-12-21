# Create Data
from .firebase_auth import *
from PayUp.firebase import db

def create_firebase_user(user):

        full_name = user['full_name'] or user['username']
        try:
            user_firebase = auth.create_user(
                uid=user['username'],
                email= user['email'],
                email_verified=False,
                password=user['password'],
                phone_number=user['phone_number'] or None,
                display_name= full_name,
                disabled=False
            )
            initialise_user_table(user['username'], displayname=full_name )               
        except Exception as e:
            raise e
            
        #print('Sucessfully created new user: {0}'.format(user_firebase.uid))
        return user_firebase

def firebase_custom_token_generator(uid: str) -> str:

    return auth.create_custom_token(uid)




def update_firebase_user(token_uid, data):
    user_data = data
    try:
        user = auth.update_user(
        token_uid,
        email=user_data['email'],
        phone_number=user_data['phone_number'],
        display_name=user_data['full_name'],

        )
    except Exception as e:
        raise e
    return user

def set_car_of_user(token_uid, car):

    car_ref = db.collection('User-Details').document(token_uid)

    if not car_ref.get().exists:
        car_ref = initialise_user_table(token_uid)
    
    user_details = car_ref.get().to_dict()
    car_data = {
        'car_model': car['car_model'],
        'mileage': car['mileage']
    }
    user_details['cars'].append(car_data)

    car_ref.set(user_details)

    return car_ref


def set_name_and_dp_of_user(token_uid, data):

    if data:
        car_ref = db.collection('User-Details').document(token_uid)

        if not car_ref.get().exists:
            car_ref = initialise_user_table(token_uid)
        user_details = car_ref.get().to_dict()
        print(data)
        if data['displayname']:
            user_details['displayname'] = data['displayname']
        if data['displaypic']:
            user_details['displaypic'] =  data['displaypic']
        car_ref.set(user_details)

        return user_details
    else:
        return None



def delete_car_of_user(token_uid, car_model):

    car_ref = db.collection('User-Details').document(token_uid)

    if not car_ref.get().exists:
        car_ref = initialise_user_table(token_uid)
    
    user_details = car_ref.get().to_dict()
    flag = 0
    for car in user_details['cars']:

        if car['car_model'] == car_model:
            user_details['cars'].remove(car)
            flag = 1

    if flag == 1:
        car_ref.set(user_details)
        return True
    else:
        return False
    
    

def add_device_token_to_user_table(reg_token, token_uid):

    user_ref = db.collection('User-Details').document(token_uid)
    user_query = user_ref.get()
    if not user_query.exists:
        user_ref = initialise_user_table(token_uid)

    user_details = user_query.to_dict()

    user_details['device_notif_token'] = reg_token

    user_ref.set(user_details)

    return user_details



# Public Functions

def initialise_user_table(uid, displayname=None, displaypic="https://firebasestorage.googleapis.com/v0/b/inout-776aa.appspot.com/o/avatar-png%2F07.png?alt=media&token=5963605e-b4e9-488c-be68-1f75c466fd8b"):
    user_ref = db.collection('User-Details').document(uid)
    user_data = {
        "rooms": [],
        "rooms_created": [],
        "cars": [],
        "address": [],  
        "displayname": displayname or uid,
        "displaypic": displaypic,
        "privacy": False
        # TODO: Add More fields when new features are added.
    }
    user_ref.set(user_data)

    return user_ref 

def get_or_create_user_table(uid):
    user_ref = db.collection('CP_ROOM').document(uid)
    if not user_ref.get().exists:
        user_ref = initialise_user_table(uid)

    return user_ref

        