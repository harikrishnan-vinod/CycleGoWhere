from flask import Flask, session, request, jsonify
from flask_cors import CORS
import pyrebase

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

@app.route("/auth", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session["user"] = email
        return jsonify({"message": "Login successful", "userId": user["localId"], "email": email})
    except Exception as e:
        print(f"Login failed: {e}")
        return jsonify({"message": "Wrong email or password"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logout successful"})

if __name__ == "__main__":
    app.run(port=1234, debug=True)