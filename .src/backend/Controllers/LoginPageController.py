from flask import request, jsonify
from firebase_admin import auth as admin_auth
from firebase_admin import firestore
from Controllers.SessionController import SessionController
from Entities.User import User
from Entities.Settings import Settings
from Entities.DatabaseController import DatabaseController
from authentication.authentication import pyrebase_auth

class LoginPageController:
    def __init__(self):
        self.db_controller = DatabaseController()
        self.session_controller = SessionController()
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
                
                # Create username mapping
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
                
            # Create user with Pyrebase
            user = self.auth.create_user_with_email_and_password(email, password)
            user_UID = user["localId"]
            
            # Store user in Firestore
            self.db_controller.db.collection("users").document(user_UID).set({ # TODO: Create a method in database controller to do this
                "email": email,
                "username": username,
                "firstName": first_name,
                "lastName": last_name,
                "profilePic": "",
                "savedRoutes": ["", "", "", "", ""],
                "notification_enabled": True,
                "created_at": firestore.SERVER_TIMESTAMP
            })
            
            # Create username mapping TODO: Create a method in database controller to do this
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