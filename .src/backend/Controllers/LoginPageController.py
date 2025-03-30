import firebase_admin
import pyrebase
from flask import request, jsonify
from firebase_admin import auth, credentials
from Controllers.SessionController import SessionController
from Entities.User import User
from Entities.Settings import Settings
from Entities.DatabaseController import DatabaseController

class LoginPageController:
    def __init__(self, firebase):
        self.db_controller = DatabaseController()
        self.session_controller = SessionController()
        self.auth = firebase.auth()
        
    def login(self, session, login_input, password):
        if "@" in login_input:
            email = login_input
        else:
            # Lookup username → email
            username_doc = self.db_controller.db.collection("usernames").document(login_input).get() # TODO: Use database_controller method instead
            if username_doc.exists:
                email = username_doc.to_dict().get("email")
            else:
                return jsonify({"message": "Wrong username or password"}), 401

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            user_UID = user["localId"]

            # Get username from userUID document (new structure)
            user_doc = self.db_controller.db.collection("users").document(user_UID).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                username = user_data.get("username", "")
            else:
                return jsonify({"message": "User record not found"}), 404
            session["user"] = email
            # email = user["email"]
            # uid = user["localId"]
            # settings = Settings(self.db_controller.get_notifications_enabled(username),
            #                     self.db_controller.get_profile_picture(username))
            # activities = self.db_controller.get_activities(username) # TODO: Method might not be correctly implemented
            # saved_routes = self.db_controller.get_saved_routes(username) # TODO: Method might not be correctly implemented
            
            # Create user object
            # user_obj = User(uid=user["localId"],
            #                 email=user["email"],
            #                 username=username,
            #                 settings=Settings(notification_enabled=settings.get_notification_enabled()),
            #                 # activities, #TODO: To be implemented
            #                 # saved_routes
            #                 )
            # Store user object in session
            # self.session_controller.set_user_session(user_obj)

            print(f"uid: {user['localId']}")
            print(f"session: {session}")

            return jsonify({
                "message": "Login successful",
                "userUID": user_UID,
                "email": email,
                "username": username
            }), 200
        
        except Exception as e:
            print("Login failed:", e)
            return jsonify({"message": "Wrong username or password"}), 401

 
        # try:
        #     # Firebase authentication
        #     user = auth.get_user_by_email(email)
        #     # Return user data from database
        #     return self.db_controller.get_user_by_id(user.UID)
        # except Exception as e:
        #     return {"error": str(e)}, 401

    def logout(self, session):
        session.pop("user", None)
        session.pop("user_id", None)
        return jsonify({"message": "Logout successful"})
    
    def register(self, email, username, password):
        try:
            # Check if username exists
            if self.db_controller.username_exists(username):
                return {"error": "Username already exists"}, 400
                
            # Create user in Firebase Auth
            user = auth.create_user(
                email=email,
                password=password
            )
            
            # Create user in database
            new_user = User(user.UID, email, username)
            self.db_controller.add_user(new_user)
            
            return {"message": "User created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 400
    
    def forgot_password(self, email):
        try:
            # Send password reset email via Firebase
            auth.generate_password_reset_link(email)
            return {"message": "Password reset link sent"}, 200
        except Exception as e:
            return {"error": str(e)}, 400