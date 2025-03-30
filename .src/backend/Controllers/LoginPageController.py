from flask import request, jsonify
#from firebase_admin import auth as admin_auth
from Entities.User import User
from Entities.DatabaseController import DatabaseController
from authentication import pyrebase_auth
from authentication.authentication import pyrebase_auth


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
                username_doc = self.db_controller.db.collection("usernames").document(login_input).get()
                if username_doc.exists:
                    email = username_doc.to_dict().get("email")
                else:
                    return jsonify({"message": "Wrong username or password"}), 401

            # Authenticate with Firebase
            user = self.auth.sign_in_with_email_and_password(email, password)
            user_UID = user["localId"]
            
            # Get id token for session
            id_token = user['idToken']

            # Get username from userUID document
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
                
                # Create username mapping
                self.db_controller.db.collection("usernames").document(username).set({
                    "email": email,
                    "userUID": user_UID
                })

            # Store user info in session
            session["user"] = email
            session["user_UID"] = user_UID
            session["id_token"] = id_token

            return jsonify({
                "message": "Login successful",
                "userUID": user_UID,
                "email": email,
                "username": username
            })
        except Exception as e:
            print("Login failed:", str(e))
            return jsonify({"message": "Wrong username or password"}), 401
    
    def register(self, email, username, password):
        try:
            # Check if username exists in Firestore
            username_doc = self.db_controller.db.collection("usernames").document(username).get()
            if username_doc.exists:
                return jsonify({"message": "Username already exists"}), 400
                
            # Create user with Pyrebase
            user = self.auth.create_user_with_email_and_password(email, password)
            user_UID = user["localId"]
            
            # Store user in Firestore
            self.db_controller.db.collection("users").document(user_UID).set({
                "email": email,
                "username": username
            })
            
            # Create username mapping
            self.db_controller.db.collection("usernames").document(username).set({
                "email": email,
                "userUID": user_UID
            })
            
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