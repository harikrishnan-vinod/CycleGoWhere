import firebase_admin
import pyrebase
from flask import request, jsonify
from firebase_admin import auth, credentials
from Entities.User import User
from Entities.Settings import Settings
from Entities.DatabaseController import DatabaseController

class LoginPageController:
    def __init__(self, firebase):
        self.db_controller = DatabaseController()
        self.auth = firebase.auth()
        
    def login(self, session, login_input, password):
        if "@" in login_input:
            email = login_input
        else:
            username_doc = self.db_controller.db.collection("usernames").document(login_input).get() # TODO: Use database_controller method instead
        if username_doc.exists:
            email = username_doc.to_dict().get("email")
        else:
            return jsonify({"message": "Wrong username or password"}), 401

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            username = login_input if "@" not in login_input else None

            if username is None:
                users_ref = self.db_controller.db.collection("usernames").stream()
                for doc_snapshot in users_ref:
                    doc = doc_snapshot.to_dict()
                    if doc.get("email") == email:
                        username = doc_snapshot.id
                        break

            # session["user"] = email
            uid = user["localId"]
            email = user["email"]
            session[uid] = {username, email, }

            print(f"user: {user}") #TODO: This is the UserUID in the firestor Can use this as key for user session
            print(f"session{session}")
            ###TESTING###
            # uid = self.db_controller.get_uid_by_username(username) # TODO: Might not be necessary, remove?
            # user.set_username(username)
            # notification_enabled = self.db_controller.get_notifications_enabled(username)
            # profile_picture = self.db_controller.get_profile_picture(username)
            # settings = Settings(notification_enabled, profile_picture)
            # saved_routes = self.db_controller.get_saved_routes(username) # TODO: Method might not be correctly implemented
            # activities = self.db_controller.get_activities(username) # TODO: Method might not be correctly implemented
            #############
            return jsonify({
                "message": "Login successful",
                "userId": user["localId"],
                "email": email,
                "username": username
            }), 200
        
        except Exception as e:
            print("Login failed:", e)
            return jsonify({"message": "Wrong username or password"}), 401
            # return None, jsonify({"message": "Wrong username or password"}), 401
 
        # try:
        #     # Firebase authentication
        #     user = auth.get_user_by_email(email)
        #     # Return user data from database
        #     return self.db_controller.get_user_by_id(user.uid)
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
            new_user = User(user.uid, email, username)
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