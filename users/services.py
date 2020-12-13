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

def set_addresss_user(token_uid, address):

    address_ref = db.collection('User-Details').document(token_uid).set(address)
    return address_ref
    