# Create Data
from .firebase_auth import *
from PayUp.firebase import db

def create_firebase_user(user):
        try:
            user_firebase = auth.create_user(
                uid=user['username'],
                email= user['email'],
                email_verified=False,
                password=user['password'],
                phone_number=user['phone_number'],
                display_name= user['full_name'],
                disabled=False
            )
            initialise_user_table(user['username'])
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

def get_car_of_user(token_uid):

    car_ref = db.collection('User-Details').document(token_uid)
    if not car_ref.get().exists:
        car_ref = initialise_user_table(token_uid)    
    car_details = car_ref.get().to_dict()

    return  {'cars': car_details['cars']}



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
    
    


def initialise_user_table(uid)-> str:
    user_ref = db.collection('User-Details').document(uid)
    user_data = {
        "rooms": [],
        "rooms_created": [],
        "cars": [],
        "address": [],  
        # TODO: Add More fields when new features are added.
    }
    user_ref.set(user_data)

    return user_ref



# Public Functions

def get_or_create_user_table(uid):
    user_ref = db.collection('CP_ROOM').document(uid)
    if not user_ref.get().exists:
        user_ref = initialise_user_table(uid)

    return user_ref

        