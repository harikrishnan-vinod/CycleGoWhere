from flask import Flask, session, request, jsonify, redirect, url_for
from flask_cors import CORS
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account
from datetime import datetime, timedelta

# Import controllers
from Controllers.LoginPageController import LoginPageController
from Controllers.MainPageController import MainPageController
from Controllers.ProfilePageController import ProfilePageController
from Controllers.SavedRoutesController import SavedRoutesController
from Controllers.SettingsPageController import SettingsPageController

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

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    try:
        auth.send_password_reset_email(email)
        return jsonify({"message": "Password reset link sent"})
    except Exception as e:
        return jsonify({"message": "Email not found"}), 404

# Main page routes
@app.route('/api/search-route', methods=['POST'])
def search_route():
    data = request.get_json()
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    return main_controller.search_route(data.get('from_location'), data.get('to_location'), user_id)

@app.route('/api/filter-map', methods=['POST'])
def filter_map():
    data = request.get_json()
    return main_controller.filter_map(data.get('filter_options'))

@app.route('/api/navigate-route/<route_id>', methods=['GET'])
def navigate_route(route_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    return main_controller.navigate_route(route_id, user_id)

@app.route('/api/check-weather', methods=['POST'])
def check_weather():
    data = request.get_json()
    route = data.get('route')
    return main_controller.check_weather(route)

# Profile page routes
@app.route('/api/cycling-statistics', methods=['GET'])
def cycling_statistics():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    period = request.args.get('period', 'week')
    return profile_controller.get_cycling_statistics(user_id, period)

@app.route('/api/personal-best', methods=['GET'])
def personal_best():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    return profile_controller.get_personal_best(user_id)

@app.route('/api/recent-activities', methods=['GET'])
def recent_activities():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    limit = request.args.get('limit', 3, type=int)
    return profile_controller.get_recent_activities(user_id, limit)

@app.route('/api/ride-history', methods=['GET'])
def ride_history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    return profile_controller.get_all_ride_history(user_id)

@app.route('/api/ride-history/<activity_id>', methods=['DELETE'])
def delete_ride(activity_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    return profile_controller.delete_ride_history(user_id, activity_id)

# Saved routes routes
@app.route('/api/saved-routes', methods=['GET'])
def saved_routes():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    return saved_routes_controller.get_saved_routes(user_id)

@app.route('/api/save-route', methods=['POST'])
def save_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    data = request.get_json()
    return saved_routes_controller.save_route(user_id, data.get('route_id'))

@app.route('/api/unsave-route', methods=['POST'])
def unsave_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    data = request.get_json()
    return saved_routes_controller.unsave_route(user_id, data.get('route_id'))

@app.route('/api/start-activity/<route_id>', methods=['GET'])
def start_activity(route_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    return saved_routes_controller.start_activity_from_saved(user_id, route_id)

# Settings routes
@app.route('/api/user-settings', methods=['GET', 'PUT'])
def user_settings():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    if request.method == 'GET':
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return jsonify({
                "email": user_data.get('email'),
                "username": user_data.get('username'),
                "notification_enabled": user_data.get('notification_enabled', True)
            })
        return jsonify({"message": "User not found"}), 404
    
    elif request.method == 'PUT':
        data = request.get_json()
        return settings_controller.manage_user_account_settings(user_id, data)

@app.route('/api/notifications', methods=['PUT'])
def toggle_notification():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    data = request.get_json()
    return settings_controller.toggle_notification(user_id, data.get('notification_enabled'))

# Activity tracking routes
@app.route('/api/activity', methods=['POST'])
def record_activity():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401
    
    data = request.get_json()
    
    # Get user reference
    user_ref = db.collection('users').document(user_id)
    
    # Create activity document
    activity_data = {
        'user_id': user_id,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'start_time': data.get('start_time'),
        'end_time': data.get('end_time'),
        'distance': data.get('distance', 0),
        'duration': data.get('duration', 0),
        'calories': data.get('calories', 0),
        'average_speed': data.get('average_speed', 0),
        'max_speed': data.get('max_speed', 0),
        'route': data.get('route', {}),
    }
    
    # Save to Firestore
    new_activity_ref = db.collection('activities').document()
    new_activity_ref.set(activity_data)
    
    # Add to user's activities
    user_ref.update({
        'activities': firestore.ArrayUnion([new_activity_ref.id])
    })
    
    return jsonify({
        "message": "Activity recorded successfully",
        "activity_id": new_activity_ref.id
    }), 201

if __name__ == "__main__":
    app.run(port=1234, debug=True)