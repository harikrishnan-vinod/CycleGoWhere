from firebase_admin import firestore
from firebase_admin import credentials, firestore, auth as firebase_auth
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import pyrebase
import firebase_admin

load_dotenv()  # Load environment variables from .env file

# Add this after load_dotenv()
required_env_vars = [
    "FIREBASE_API_KEY", 
    "FIREBASE_AUTH_DOMAIN", 
    "FIREBASE_PROJECT_ID",
    "FIREBASE_STORAGE_BUCKET", 
    "FIREBASE_MESSAGING_SENDER_ID", 
    "FIREBASE_APP_ID",
    "FIREBASE_DATABASE_URL"
]

for var in required_env_vars:
    if not os.environ.get(var):
        raise EnvironmentError(f"Required environment variable {var} is missing")

# Get configuration from environment variables
config = {
    "apiKey": os.environ.get("FIREBASE_API_KEY"),
    "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
    "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.environ.get("FIREBASE_APP_ID"),
    "databaseURL": os.environ.get("FIREBASE_DATABASE_URL")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Initialize Firebase Admin SDK (only once)
try:
    # If already initialized, this will raise an exception
    default_app = firebase_admin.get_app()
except ValueError:
    # Use environment variable for service account path
    service_account_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT_PATH')
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)

# Export the auth instances for use in other files
pyrebase_auth = auth
admin_sdk_auth = firebase_auth

db = firestore.client()
firestore_module = firestore

__all__ = ['db', 'firestore_module']