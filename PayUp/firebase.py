# Firebase Variables

import firebase_admin
from firebase_admin import credentials, firestore, messaging
from datetime import datetime
if not firebase_admin._apps:
    cred = credentials.Certificate("./firebasekey.json")
    firebase_admin.initialize_app(cred)

GeoPoint = firestore.GeoPoint
db = firestore.client()



sign_in_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
token_refresh_url = "https://securetoken.googleapis.com/v1/token"


# Custom Helper Functions

def unique_key_generator(key_len):
    # By Sandeep Pillai
    if key_len > 10:
        raise ValueError("Cannot Generate a key over length 10")

    now = datetime.now() # current date and time
    time_string = now.strftime("%H%M%S%f%Y%m%d")
    time_string = time_string[0:(key_len*2)]
    key_string = ""
    for index in range(0, len(time_string), 2):
        val = time_string[index:index+2]
        key_string += chr(65 + int(val)%26)


    return str(key_string)

