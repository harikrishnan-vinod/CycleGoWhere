from flask import request, jsonify
from firebase_admin import auth
from Entities.Settings import Settings
from Entities.DatabaseController import DatabaseController
from routes.services import cloudinary, pyrebase_auth, firebase_auth
import requests
import os

class SettingsPageController:

    def __init__(self):
        self.db_controller = DatabaseController()

    def change_profile_pic(self):
        if 'file' not in request.files or 'userUID' not in request.form:
            return {"message": "Missing file or userUID"}, 400

        file = request.files['file']
        user_UID = request.form['userUID']

        try:
            result = cloudinary.uploader.upload(file, folder="profilePictures")
            image_url = result.get("secure_url")
        except Exception as e:
            print("Upload failed:", e)
            return {"message": "Upload to Cloudinary failed"}, 500
        
        return self.db_controller.update_user_profile_picture(user_UID, image_url)
    

    def change_user_password(self, FIREBASE_API_KEY, email, old_password, new_password):
        try:
            user = pyrebase_auth.sign_in_with_email_and_password(email, old_password)

            id_token = user["idToken"]
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={FIREBASE_API_KEY}"

            payload = {
                "idToken": id_token,
                "password": new_password,
                "returnSecureToken": True
            }

            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return jsonify({"message": "Password updated successfully"}), 200
            else:
                print("Failed:", response.json())
                return jsonify({"message": "Failed to update password"}), 400

        except Exception as e:
            print("Error changing password:", e)
            return jsonify({"message": "Authentication failed"}), 401
        

    def change_email(self, user_UID, new_email):
        try:
            firebase_auth.update_user(user_UID, email=new_email)
            self.db_controller.update_user_email(user_UID, new_email)

            return jsonify({"message": "Email updated"}), 200
        except Exception as e:
            print("Email change failed:", e)
            return jsonify({"message": "Failed to update email"}), 500
        

    def change_username(self, user_UID, new_username):
        if self.db_controller.username_exists(new_username):
            return jsonify({"message": "Username already exists"}), 400

        try:
            return self.db_controller.update_username(user_UID, new_username)
        
        except Exception as e:
            print("Username change failed:", e)
            return jsonify({"message": "Update failed"}), 500

    
    def manage_user_account_settings(self, user_id, settings_data):
        try:
            # Update user settings
            if "username" in settings_data:
                # Check if username exists and is different from current
                if self.db_controller.username_exists(settings_data["username"]) and \
                   self.db_controller.get_user_username(user_id) != settings_data["username"]:
                    return {"error": "Username already exists"}, 400
                
                # Update username
                self.db_controller.update_user_username(user_id, settings_data["username"])
            
            if "email" in settings_data:
                # Update email in Firebase Auth
                auth.update_user(user_id, email=settings_data["email"])
                
                # Update email in database
                self.db_controller.update_user_email(user_id, settings_data["email"])
            
            if "password" in settings_data:
                # Update password in Firebase Auth
                auth.update_user(user_id, password=settings_data["password"])
            
            if "profile_picture" in settings_data:
                # Update profile picture
                self.db_controller.update_user_profile_picture(user_id, settings_data["profile_picture"])
            
            return {"message": "User settings updated successfully"}
        except Exception as e:
            return {"error": str(e)}, 400
    
    def toggle_notification(self, user_id, notification_enabled):
        try:
            # Update notification settings
            self.db_controller.update_notification_settings(user_id, notification_enabled)
            
            return {"message": "Notification settings updated successfully"}
        except Exception as e:
            return {"error": str(e)}, 400