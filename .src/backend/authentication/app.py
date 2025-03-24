from flask import Flask, session, request, jsonify, redirect, url_for
from flask_cors import CORS
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import id_token
from google.auth.transport import requests
from google.oauth2 import service_account


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
  "databaseURL" :""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

cred = credentials.Certificate(".src/backend/authentication/work.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    print("hello world")
    return jsonify({"message": "Logout successful"}), 200

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

    token_response = requests.Request().session.post(token_url, data=payload)
    token_response_json = token_response.json()

    if 'id_token' in token_response_json:
        id_info = id_token.verify_oauth2_token(
            token_response_json['id_token'],
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = id_info.get('email')
        user_uid = id_info.get('sub')

        session["user"] = email
        return redirect('http://localhost:5173/mainpage')

    return jsonify({"message": "Google login failed"}), 400



if __name__ == "__main__":
    app.run(port=1234, debug=True)