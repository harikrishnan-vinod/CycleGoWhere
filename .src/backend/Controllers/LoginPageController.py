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
                username_doc = self.db_controller.db.collection("usernames").document(login_input).get() # TODO: Use database_controller method instead
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
            # Get user settings
            settings = Settings(self.db_controller.get_notifications_enabled(user_UID),
                                self.db_controller.get_profile_picture(user_UID))
            
            # Get user activities
            # activities = self.db_controller.get_activities(username) # TODO: Method might not be correctly implemented

            # Get user saved routes
            # saved_routes = self.db_controller.get_saved_routes(username) # TODO: Method might not be correctly implemented
            
            # Create user object
            user_obj = User(uid=user_UID,
                            email=user["email"],
                            username=username,
                            settings=Settings(notification_enabled=settings.get_notification_enabled(),
                                              profile_picture=settings.get_profile_picture()),
                            # activities, #TODO: To be implemented
                            # saved_routes
                            )
            print("User object created")

            # Store user object in session
            self.session_controller.set_user_session(user_obj)
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
            username_doc = self.db_controller.db.collection("usernames").document(username).get()
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