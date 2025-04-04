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

    def get_username(self, user_UID):
        if not user_UID:
            return jsonify({"message": "User UID required"}), 400

        try:
            username = self.db_controller.get_username_by_uid(user_UID)
            if username:
                return jsonify({"username": username}), 200
            else:
                return jsonify({"message": "Username not found"}), 404
        except Exception as e:
            print("Error fetching username:", e)
            return jsonify({"message": "Server error"}), 500
        
    def get_profile_pic(self, user_UID):
        if not user_UID:
            return jsonify({"message": "User UID required"}), 400

        try:
            profile_pic = self.db_controller.get_profile_picture(user_UID)
            if not profile_pic == '':
                return jsonify({"profilePic": profile_pic}), 200
            else:
                return jsonify({"message": "Profile picture not found"}), 404
        except Exception as e:
            print("Error fetching profile picture:", e)
            return jsonify({"message": "Server error"}), 500

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

    
    def toggle_notification(self, user_id, notification_enabled): #TODO: 
        try:
            # Update notification settings
            self.db_controller.update_notification_settings(user_id, notification_enabled)
            
            return {"message": "Notification settings updated successfully"}
        except Exception as e:
            return {"error": str(e)}, 400