import pyrebase
import os
from dotenv import load_dotenv
load_dotenv(override=True)


class FirebaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            firebase_config = {
                "apiKey": os.getenv("FIREBASE_API_KEY"),
                "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
                "projectId": os.getenv("FIREBASE_PROJECT_ID"),
                "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
                "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
                "appId": os.getenv("FIREBASE_APP_ID"),
                "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
                "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
            }

            firebase = pyrebase.initialize_app(firebase_config)
            cls._auth = firebase.auth()
            cls._db = firebase.database()
        return cls._instance

    @property
    def auth(self):
        return self._auth

    @property
    def db(self):
        return self._db
