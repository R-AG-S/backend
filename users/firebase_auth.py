# Import this to any API file that requires user authentication with tokens.
# from users.firebase_auth import *
import firebase_admin # Dunno why, but it doens't work without this import.
from firebase_admin import credentials, firestore, auth, _token_gen

if not firebase_admin._apps:
    cred = credentials.Certificate("./firebasekey.json")
    firebase_admin.initialize_app(cred)






