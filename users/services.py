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

def set_car_of_user(token_uid, address):

    address_ref = db.collection('User-Details').document(token_uid).set(address)
    return address_ref
    


def initialise_user_table(uid)-> str:
    user_ref = db.collection('User-Details').document(uid)
    user_data = {
        "rooms": [],
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

        