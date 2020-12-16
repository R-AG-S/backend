# Fetch data
import json
from decouple import config
import requests
from .firebase_auth import * 
from PayUp.firebase import db, sign_in_url, token_refresh_url

# Stored in .env file in root of project. Retrieve from Firebase Console, Settings -> General -> Web API Keys  
# and add to your .env file as follows: 
# FIREBASE_WEB_API_KEY=ABCDERFTIOEJFOCIJOFISJO (without quotes.)
FIREBASE_WEB_API_KEY = config('FIREBASE_WEB_API_KEY') 
            


# Public Functions

def obj_to_json(obj):
    return json.dumps(obj.__dict__['_data'])


def get_uid_from_token(idToken: str)->str:      # User_Id or None
    try:
        decoded_token = auth.verify_id_token(idToken)
        uid = decoded_token['uid']
    except:
        uid = None
    return uid

def get_user_data_from_uid(uid: str):
    try:
        user = auth.get_user(uid)

    except:
        user = None

    return user



# Private Functions

def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):

    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(sign_in_url,
                      params = {"key": FIREBASE_WEB_API_KEY},
                      data = payload)

    return r


def firebase_refresh_token(refreshToken: str):
    print('test', refreshToken)
    payload = json.dumps({
        "grant_type": "refresh_token",
        "refresh_token": refreshToken
    })

    r = requests.post(token_refresh_url,
                      params = {"key": FIREBASE_WEB_API_KEY},
                      data = payload)
    print(r)
    return r 


def get_additional_user_data(uid):

    additional_user_data = db.collection('User-Details').document(uid).get()
    return additional_user_data

def getuserlist( ): # max_results -> how many users per function call. offset -> which page to paginate from,

    page = auth.list_users()
    user_id_list = []
    while page:
        for user in page.users:
            user_id_list.append(user)
        # Get next batch of users.
        page = page.get_next_page()

    return user_id_list
        

def user_list_slicer(user_id_list, offset:int, page_size: int):
    user_slice = user_id_list[offset:offset+page_size] # Python List slicing
    return user_slice


def paginate_user_list(offset:int, page_size: int):
    all_users = getuserlist()
    page_slice = user_list_slicer(all_users, offset, page_size)

    user_dict = {}
    for item in page_slice:
        user_dict[item.uid] = item

    return user_dict



