from flask import Blueprint, request, jsonify
import requests
from .services import db , cloudinary, pyrebase_auth, firebase_auth
import os
from Controllers.SettingsPageController import SettingsPageController

setting_bp = Blueprint("setting",__name__)
settings_controller = SettingsPageController()

@setting_bp.route("/upload-profile-pic", methods=["POST"])
def upload_profile_pic():
    return settings_controller.change_profile_pic()


# get first name
@setting_bp.route("/get-username")
def get_username():
    user_UID = request.args.get("userUID")
    return settings_controller.get_username(user_UID)
    

@setting_bp.route("/get-profile-pic")
def get_profile_pic():
    user_UID = request.args.get("userUID")
    return settings_controller.get_profile_pic(user_UID)

    
@setting_bp.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json()
    email = data.get("email")
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    return settings_controller.change_user_password(os.environ.get('FIREBASE_API_KEY'),
                                                       email,
                                                       old_password,
                                                       new_password)

@setting_bp.route("/change-email", methods=["POST"])
def change_email():
    data = request.get_json()
    UID = data.get("userUID")
    new_email = data.get("newEmail")

    return settings_controller.change_email(UID, new_email)


@setting_bp.route("/change-username", methods=["POST"])
def change_username():
    data = request.get_json()
    UID = data.get("userUID")
    new_username = data.get("newUsername")

    return settings_controller.change_username(UID, new_username)