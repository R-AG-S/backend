import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


sign_in_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
token_refresh_url = "https://securetoken.googleapis.com/v1/token"