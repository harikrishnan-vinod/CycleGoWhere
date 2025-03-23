from flask import Flask, session, request, jsonify
from flask_cors import CORS
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'fhsidstuwe59weirwnsj099w04i5owro'
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


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

cred = credentials.Certificate("work.json")
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
    return jsonify({"message": "Logout successful"})

if __name__ == "__main__":
    app.run(port=1234, debug=True)