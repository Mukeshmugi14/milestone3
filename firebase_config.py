"""
CodeGalaxy - Firebase Configuration
Initializes Firebase Admin SDK for authentication and Firestore.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

db = None

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK for Firestore and Pyrebase for authentication.
    """
    global db

    # Firebase Admin SDK Configuration for Firestore
    service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT')

    if service_account_path and os.path.exists(service_account_path):
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()

    # Pyrebase Configuration for client-side authentication
    firebase_config = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    }

    firebase = pyrebase.initialize_app(firebase_config)
    return firebase.auth()
