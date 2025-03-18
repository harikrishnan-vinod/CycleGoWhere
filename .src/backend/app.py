from flask import Flask, session, request, jsonify
from flask_cors import CORS
import pyrebase

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
app.secret_key = 'fhsidstuwe59weirwnsj099w04i5owro'

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

@app.route("/auth", methods=['POST', 'OPTIONS'])  # Handle CORS preflight request
def login():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session["user"] = email  # Store session
        return _build_cors_response(jsonify({"message": "Login successful", "userId": user["localId"], "email": email}))
    except:
        return _build_cors_response(jsonify({"message": "Wrong email or password"}), 401)

@app.route("/logout", methods=["POST", "OPTIONS"])
def logout():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    session.pop("user", None)
    return _build_cors_response(jsonify({"message": "Logout successful"}))

# Helper functions for CORS
def _build_cors_response(response):
    """Adds CORS headers to the response."""
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

def _build_cors_preflight_response():
    """Handles the CORS preflight request."""
    response = jsonify({"message": "CORS preflight successful"})
    return _build_cors_response(response)

if __name__ == "__main__":
    app.run(port=1234, debug=True)