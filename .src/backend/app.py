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
import cloudinary
import cloudinary.uploader

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

app.config.update(
    SESSION_COOKIE_SAMESITE='None',  # Allow cookies for cross-origin requests
    SESSION_COOKIE_SECURE=True,      # Ensure cookies are sent over HTTPS
    PERMANENT_SESSION_LIFETIME=timedelta(days=1)  # Set session lifetime (optional)
)
cloudinary.config(
  cloud_name = "dp75ekaxp",
  api_key = "REMOVED",
  api_secret = "REMOVED"
)

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

login_controller = LoginPageController(firebase)
main_controller = MainPageController()
profile_controller = ProfilePageController()
saved_routes_controller = SavedRoutesController()
settings_controller = SettingsPageController()

@app.route("/auth", methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get("login")
    password = data.get("password")
    return login_controller.login(session, login_input, password)

    if "@" in login_input:
        email = login_input
    else:
        username_doc = db.collection("usernames").document(login_input).get()
        if username_doc.exists:
            email = username_doc.to_dict().get("email")
        else:
            return jsonify({"message": "Wrong username or password"}), 401

    try:
        user = auth.sign_in_with_email_and_password(email, password)


        username = login_input if "@" not in login_input else None

        if username is None:
            users_ref = db.collection("usernames").stream()
            for doc_snapshot in users_ref:
                doc = doc_snapshot.to_dict()
                if doc.get("email") == email:
                    username = doc_snapshot.id
                    break

        session["user"] = email
        return jsonify({
            "message": "Login successful",
            "userId": user["localId"],
            "email": email,
            "username": username
        })
    except Exception as e:
        print("Login failed:", e)
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
    first_name = data.get("firstName", "")
    last_name = data.get("lastName", "")

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

        db.collection("users").document(username).set({
            "email": email,
            "username": username,
            "firstName": first_name,
            "profilePic": "",
            "lastName": last_name,
            "savedRoutes": ["", "", "", "", ""],
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
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=5
        )

        email = id_info.get('email')
        user_uid = id_info.get('sub')
        full_name = id_info.get('name', '')
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user_doc = db.collection("users").where("email", "==", email).get()
        if not user_doc:
            username = email.split('@')[0]  
            username_count = 0
            base_username = username
            while db.collection("usernames").document(username).get().exists:
                username_count += 1
                username = f"{base_username}{username_count}"

            db.collection("usernames").document(username).set({
                "email": email,
                "userUID": user_uid
            })

            db.collection("users").document(username).set({
                "email": email,
                "username": username,
                "firstName": first_name,
                "profilePic":"",
                "lastName": last_name,
                "savedRoutes": ["", "", "", "", ""],
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
        try:
            data = search.searchRequest(fromAddress,token)
            return data

        except Exception as e:
            return jsonify({'error':'internal server error'}) 

        
    if destAddress:
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
    

@app.route('/fetchWaterPoint', methods=["POST"])
def getWaterPoint():
    data = request.json
    instructions = data.get("routeInstructions", [])

    points = []
    for step in instructions:
        latlng_str = step[3]
        if latlng_str:
            try:
                lat_str, lng_str = latlng_str.split(",")
                lat, lng = float(lat_str), float(lng_str)
                points.append((lat, lng))  # ✅ now a list of (lat, lng) tuples
            except ValueError:
                continue 
        
    result = search.findWaterPoints(points,csv_path="./helperFunctions/verified_points.csv")
    return result


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

@app.route("/upload-profile-pic", methods=["POST"])
def upload_profile_pic():
    if 'file' not in request.files or 'username' not in request.form:
        return {"message": "Missing file or username"}, 400

    file = request.files['file']
    username = request.form['username']

    try:
        result = cloudinary.uploader.upload(file, folder="profilePictures")
        image_url = result.get("secure_url")
    except Exception as e:
        print("Upload failed:", e)
        return {"message": "Upload to Cloudinary failed"}, 500

    try:
        db.collection("users").document(username).update({
            "profilePic": image_url
        })
        return {"message": "Profile picture updated", "url": image_url}, 200
    except Exception as e:
        print("Firestore update failed:", e)
        return {"message": "Failed to update Firestore"}, 500
    
@app.route("/get-profile-pic")
def get_profile_pic():
    username = request.args.get("username")
    if not username:
        return jsonify({"message": "Username required"}), 400

    try:
        doc = db.collection("users").document(username).get()
        if doc.exists:
            return jsonify({"profilePic": doc.to_dict().get("profilePic")}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Error fetching profile picture:", e)
        return jsonify({"message": "Server error"}), 500
    
@app.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json()
    email = data.get("email")
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")

    try:
        user = auth.sign_in_with_email_and_password(email, old_password)

        id_token = user["idToken"]
        url = "https://identitytoolkit.googleapis.com/v1/accounts:update?key=REMOVED"

        payload = {
            "idToken": id_token,
            "password": new_password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return jsonify({"message": "Password updated successfully"}), 200
        else:
            print("Failed:", response.json())
            return jsonify({"message": "Failed to update password"}), 400

    except Exception as e:
        print("Error changing password:", e)
        return jsonify({"message": "Authentication failed"}), 401






if __name__ == "__main__":
    app.run(port=1234, debug=True)