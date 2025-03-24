from flask import request, jsonify
import firebase_admin
from firebase_admin import auth
from Entities.Settings import Settings
from Entities.DatabaseController import DatabaseController

class SettingsPageController:
    def __init__(self):
        self.db_controller = DatabaseController()
    
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