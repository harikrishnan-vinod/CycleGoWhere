from flask import Flask, session, request, jsonify, redirect, url_for
from flask_cors import CORS
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account

# Import controllers
from Controllers.LoginPageController import LoginPageController
from Controllers.MainPageController import MainPageController
from Controllers.ProfilePageController import ProfilePageController
from Controllers.SavedRoutesController import SavedRoutesController
from Controllers.SettingsPageController import SettingsPageController

import time
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

#Import helper Functions
from helperFunctions import search  
load_dotenv()

auth_token = {
    "token": None,
    "expires_at": 0
}

app = Flask(__name__)
app.secret_key = 'fhsidstuwe59weirwnsj099w04i5owro'
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}}, supports_credentials=True)
GOOGLE_CLIENT_ID = 'REMOVED'

config = {
    "apiKey": "REMOVED",
    "authDomain": "REMOVED.firebaseapp.com",
    "projectId": "REMOVED",
    "storageBucket": "REMOVED",
    "messagingSenderId": "REMOVED",
    "appId": "1:REMOVED:web:496edabac517dfff8e3062",
    "databaseURL": ""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

cred = credentials.Certificate("work.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize controllers
login_controller = LoginPageController()
main_controller = MainPageController()
profile_controller = ProfilePageController()
saved_routes_controller = SavedRoutesController()
settings_controller = SettingsPageController()

# Existing auth routes
@app.route("/auth", methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get("login")
    password = data.get("password")

    if "@" in login_input:
        email = login_input
    else:
        username_doc = db.collection("usernames").document(login_input).get()

        if username_doc.exists:
            email = username_doc.to_dict().get("email")
        else:
            print(f"No username found for {login_input}")
            return jsonify({"message": "Wrong username or password"}), 401

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session["user"] = email
        session["user_id"] = user["localId"]
        return jsonify({
            "message": "Login successful", 
            "userId": user["localId"], 
            "email": email
        })
    except Exception as e:
        return jsonify({"message": "Wrong username or password"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"})

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    username_doc = db.collection("usernames").document(username).get()
    if username_doc.exists:
        return jsonify({"message": "Username already exists"}), 400

    try:
        user = auth.create_user_with_email_and_password(email, password)
        user_uid = user["localId"]

        db.collection("usernames").document(username).set({
            "email": email,
            "userUID": user_uid
        })

        # Create user document in 'users' collection
        db.collection("users").document(user_uid).set({
            "email": email,
            "username": username,
            "notification_enabled": True,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"message": "Registration successful!"}), 201

    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({"message": "Registration failed"}), 400

@app.route('/google-login')
def google_login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={url_for('google_callback', _external=True)}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )
    return redirect(google_auth_url)

@app.route('/google-callback')
def google_callback():
    code = request.args.get('code')
    token_url = 'https://oauth2.googleapis.com/token'

    payload = {
        'code': code,
        'client_id': 'REMOVED',
        'client_secret': 'REMOVED',
        'redirect_uri': url_for('google_callback', _external=True),
        'grant_type': 'authorization_code'
    }

    token_response = google_requests.Request().session.post(token_url, data=payload)
    token_response_json = token_response.json()

    if 'id_token' in token_response_json:
        id_info = id_token.verify_oauth2_token(
            token_response_json['id_token'],
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = id_info.get('email')
        user_uid = id_info.get('sub')

        # Check if user exists, if not create a new user document
        user_doc = db.collection("users").where("email", "==", email).get()
        if not user_doc:
            # Extract user info
            username = email.split('@')[0]  # Use part of email as username
            
            # Ensure username is unique
            username_count = 0
            base_username = username
            while db.collection("usernames").document(username).get().exists:
                username_count += 1
                username = f"{base_username}{username_count}"
            
            # Create username document
            db.collection("usernames").document(username).set({
                "email": email,
                "userUID": user_uid
            })
            
            # Create user document
            db.collection("users").document(user_uid).set({
                "email": email,
                "username": username,
                "notification_enabled": True,
                "created_at": firestore.SERVER_TIMESTAMP
            })

        session["user"] = email
        session["user_id"] = user_uid
        return redirect('http://localhost:5173/mainpage')

    return jsonify({"message": "Google login failed"}), 400


@app.route('/search')
def searchaddressUpdateList():
    fromAddress = request.args.get("fromAddress")
    destAddress = request.args.get("destAddress")
    token = get_onemap_token()

    
    if fromAddress:
        print("fromAddress received:", fromAddress)
        # Do something with from_address
        try:
            data = search.searchRequest(fromAddress,token)
            return data

        except Exception as e:
            return jsonify({'error':'internal server error'}) 

        
    if destAddress:
        print("fromAddress received:", destAddress)
        # Do something with from_address
        try:
            data = search.searchRequest(destAddress,token)
            return data

        except Exception as e:
            return jsonify({'error':'internal server error'}) 
        
@app.route('/route')
def handlerouting():

    fromAddress = request.args.get("fromAddress")
    destAddress = request.args.get("destAddress")
    token = get_onemap_token()
    #get latitude and longitude from onemap api
    
    try:
        data_fromAddress = search.searchAndReturnLL(fromAddress,token).get_json()
        data_destAddress = search.searchAndReturnLL(destAddress,token).get_json()
        
        combined_address = {
            "from": data_fromAddress,
            "destination": data_destAddress
        }
        
        return search.getRouting(combined_address,token)

    
    except Exception as e:
        return jsonify({'error':'internal server error'}) 


def get_onemap_token():
    """Fetch and cache the OneMap token"""
    current_time = time.time()

    if auth_token["token"] and current_time < auth_token["expires_at"]:
        return auth_token["token"]

    print("Fetching new OneMap token...")

    url = "https://www.onemap.gov.sg/api/auth/post/getToken"
    payload = {
        "email": os.environ["ONEMAP_EMAIL"],
        "password": os.environ["ONEMAP_EMAIL_PASSWORD"]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception("Failed to get OneMap token")

    data = response.json()
    token = data["access_token"]

    auth_token["token"] = token
    auth_token["expires_at"] = current_time + 24 * 60 * 60  # 24-hour expiry

    return token

if __name__ == "__main__":
    app.run(port=1234, debug=True)