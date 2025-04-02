from flask import request, jsonify, redirect, url_for
from firebase_admin import auth as admin_auth
from firebase_admin import firestore
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from Entities.User import User
from Entities.Settings import Settings
from Entities.DatabaseController import DatabaseController
from authentication.authentication import pyrebase_auth
import os

class LoginPageController:
    def __init__(self):
        self.db_controller = DatabaseController()
        self.auth = pyrebase_auth
        
    def login(self, session, login_input, password):
        try:
            if "@" in login_input:
                email = login_input
            else:
                # Lookup username → email
                email = self.db_controller.get_email_by_username(login_input)
                if email is None:
                    return jsonify({"message": "Wrong username or password"}), 401
            
                # username_doc = self.db_controller.db.collection("usernames").document(login_input).get() # TODO: Use database_controller method instead
                # if username_doc.exists:
                #     email = username_doc.to_dict().get("email")
                # else:
                #     return jsonify({"message": "Wrong username or password"}), 401

            # Authenticate with Firebase
            user = self.auth.sign_in_with_email_and_password(email, password)
            user_UID = user["localId"]
            
            # Get id token for session
            id_token = user['idToken']

            # Get username from userUID document TODO: Use database_controller method instead
            user_doc = self.db_controller.db.collection("users").document(user_UID).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                username = user_data.get("username", "")
            else:
                # Create user document if it doesn't exist
                username = email.split('@')[0]  # Default username from email
                self.db_controller.db.collection("users").document(user_UID).set({
                    "email": email,
                    "username": username
                })
                
                # Create username mapping TODO: Use database_controller method instead
                self.db_controller.db.collection("usernames").document(username).set({
                    "email": email,
                    "userUID": user_UID
                })           

            session["user"] = email
            session["user_UID"] = user_UID
            session["id_token"] = id_token

            return jsonify({
                "message": "Login successful",
                "userUID": user_UID,
                "email": email,
                "username": username
            }), 200
        
        except Exception as e:
            print("Login failed:", str(e))
            return jsonify({"message": "Wrong username or password"}), 401

    def google_login(self, google_client_id):
        try:
            google_auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={google_client_id}&"
            f"redirect_uri={url_for('google_callback', _external=True)}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile"
            )
            return redirect(google_auth_url)
        
        except Exception as e:
            print("Google login failed:", str(e))
            return jsonify({"message": "Google login failed"}), 401
        
    def google_callback(self, session, code, google_client_id, google_client_secret):
        try:
            token_url = 'https://oauth2.googleapis.com/token'

            payload = {
                'code': code,
                'client_id': google_client_id,
                'client_secret': google_client_secret,
                'redirect_uri': url_for('google_callback', _external=True),
                'grant_type': 'authorization_code'
            }

            token_response = google_requests.Request().session.post(token_url, data=payload)
            token_response_json = token_response.json()

            if 'id_token' in token_response_json:
                id_info = id_token.verify_oauth2_token(
                    token_response_json['id_token'],
                    google_requests.Request(),
                    os.environ.get('GOOGLE_CLIENT_ID'),
                    clock_skew_in_seconds=5
                )

                email = id_info.get('email')
                user_UID = id_info.get('sub')
                full_name = id_info.get('name', '')
                name_parts = full_name.split(" ", 1)
                first_name = name_parts[0] if len(name_parts) > 0 else ""
                last_name = name_parts[1] if len(name_parts) > 1 else ""

                # user_doc = self.db_controller.get_user_document(user_UID)
                if not self.db_controller.user_exists(user_UID):
                    username = email.split('@')[0]
                    base_username = username
                    counter = 0
                    while self.db_controller.username_exists(username):
                        counter += 1 # Why?
                        username = f"{base_username}{counter}"

                    user = User(uid=user_UID,
                                email=email,
                                username=username,
                                first_name=first_name,
                                last_name=last_name,
                                settings=Settings(user_UID=user_UID),
                                # activities=[],
                                # saved_routes=[]
                            )
                    if self.db_controller.add_user(user):

                        session["user"] = email
                        session["user_UID"] = user_UID

                        return redirect('http://localhost:5173/mainpage')

            return jsonify({"message": "Google login failed"}), 400

        
        except Exception as e:
            print("Google callback failed:", str(e))
            return jsonify({"message": "Google login failed"}), 401

    def logout(self, session):
        session.pop("user", None)
        session.pop("user_UID", None)
        return jsonify({"message": "Logout successful"})
    
    def register(self, email, username, password, first_name="", last_name=""):
        try:
            # Check if username exists in Firestore
            username_doc = self.db_controller.db.collection("usernames").document(username).get() # TODO: Create a method in database controller to do this
            if username_doc.exists:
                return jsonify({"message": "Username already exists"}), 400

            user = self.auth.create_user_with_email_and_password(email, password)
            user_UID = user["localId"]

            # Create user profile doc
            user_data = {
                "email": email,
                "username": username,
                "firstName": first_name,
                "lastName": last_name,
                "profilePic": "",
                "notification_enabled": True,
                "created_at": firestore.SERVER_TIMESTAMP
            }

            self.db_controller.db.collection("users").document(user_UID).set(user_data)

            self.db_controller.db.collection("usernames").document(username).set({
                "email": email,
                "userUID": user_UID
            })

            
            self.db_controller.db.collection("users").document(user_UID).collection("savedRoutes").document("dummyRoute").set({"initial": True})
            self.db_controller.db.collection("users").document(user_UID).collection("savedRoutes").document("dummyRoute").delete()

            self.db_controller.db.collection("users").document(user_UID).collection("activities").document("dummyActivity").set({"initial": True})
            self.db_controller.db.collection("users").document(user_UID).collection("activities").document("dummyActivity").delete()

            return jsonify({"message": "User created successfully", "userUID": user_UID}), 201

        except Exception as e:
            print("Registration failed:", str(e))
            return jsonify({"message": "Unable to register: " + str(e)}), 400


    
    def forgot_password(self, email):
        try:
            # Send password reset email via Pyrebase
            self.auth.send_password_reset_email(email)
            return jsonify({"message": "Password reset link sent"}), 200
        except Exception as e:
            print("Password reset failed:", str(e))
            return jsonify({"message": "Email not found or invalid"}), 400