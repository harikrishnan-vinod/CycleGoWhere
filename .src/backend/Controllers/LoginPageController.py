from flask import request, jsonify
import firebase_admin
from firebase_admin import auth, credentials
from Entities.User import User
from Entities.DatabaseController import DatabaseController

class LoginPageController:
    def __init__(self):
        self.db_controller = DatabaseController()
        
    def login(self, email, password):
        try:
            # Firebase authentication
            user = auth.get_user_by_email(email)
            # Return user data from database
            return self.db_controller.get_user_by_id(user.uid)
        except Exception as e:
            return {"error": str(e)}, 401
    
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