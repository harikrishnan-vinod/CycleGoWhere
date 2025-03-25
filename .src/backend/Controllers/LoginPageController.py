import firebase_admin
import pyrebase
from flask import request, jsonify
from firebase_admin import auth, credentials
from Entities.User import User
from Entities.DatabaseController import DatabaseController

class LoginPageController:
    def __init__(self, firebase):
        self.db_controller = DatabaseController()
        self.auth = firebase.auth()
        
    def login(self, session, login_input, password):
        if "@" in login_input:
            email = login_input
        else:
            username_doc = self.db_controller.db.collection("usernames").document(login_input).get()
        if username_doc.exists:
            email = username_doc.to_dict().get("email")
        else:
            return jsonify({"message": "Wrong username or password"}), 401

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            username = login_input if "@" not in login_input else None

            if username is None:
                users_ref = self.db_controller.db.collection("usernames").stream()
                for doc_snapshot in users_ref:
                    doc = doc_snapshot.to_dict()
                    if doc.get("email") == email:
                        username = doc_snapshot.id
                        break

            session["user"] = email
            return jsonify({
                "message": "Login successful",
                "userId": user["localId"],
                "email": email,
                "username": username
            })
        except Exception as e:
            print("Login failed:", e)
            return jsonify({"message": "Wrong username or password"}), 401
 
        # try:
        #     # Firebase authentication
        #     user = auth.get_user_by_email(email)
        #     # Return user data from database
        #     return self.db_controller.get_user_by_id(user.uid)
        # except Exception as e:
        #     return {"error": str(e)}, 401
    
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