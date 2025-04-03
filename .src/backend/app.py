from flask import Flask, session, request, jsonify, redirect, url_for
from flask_cors import CORS
from firebase_admin import credentials, firestore, auth as firebase_auth
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account
from authentication.authentication import pyrebase_auth, firebase
from authentication.authentication import admin_sdk_auth

import os
from dotenv import load_dotenv
from datetime import timedelta
import cloudinary
import cloudinary.uploader

#load routes
from routes.login_routes import login_bp
from routes.saved_routes import savedroutes_bp
from routes.search_routes import search_bp
from routes.settings_route import setting_bp
 

load_dotenv()

auth_token = {
    "token": None,
    "expires_at": 0
}

app = Flask(__name__)
app.secret_key = 'fhsidstuwe59weirwnsj099w04i5owro'
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}}, supports_credentials=True)
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

app.config.update(
    SESSION_COOKIE_SAMESITE='None',  # Allow cookies for cross-origin requests
    SESSION_COOKIE_SECURE=False,      # Ensure cookies are sent over HTTPS
    PERMANENT_SESSION_LIFETIME=timedelta(days=1)  # Set session lifetime (optional)
)

cloudinary.config(
  cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
  api_key = os.environ.get("CLOUDINARY_API_KEY"),
  api_secret = os.environ.get("CLOUDINARY_API_SECRET")
)

app.register_blueprint(login_bp)
app.register_blueprint(savedroutes_bp)
app.register_blueprint(search_bp)
app.register_blueprint(setting_bp)

if __name__ == "__main__":
    app.run(port=1234, debug=True)