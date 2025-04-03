import cloudinary
import cloudinary.uploader
from firebase_admin import firestore
from firebase_admin import credentials, firestore, auth as firebase_auth
from authentication.authentication import pyrebase_auth, firebase
from authentication.authentication import admin_sdk_auth

db = firestore.client()
firestore_module = firestore

__all__ = ['db', 'firestore_module']