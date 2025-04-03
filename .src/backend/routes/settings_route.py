from flask import Blueprint, request, jsonify
import requests
from .services import db , cloudinary, pyrebase_auth, firebase_auth
import os

setting_bp = Blueprint("setting",__name__)



@setting_bp.route("/upload-profile-pic", methods=["POST"])
def upload_profile_pic():
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

    try:
        db.collection("users").document(user_UID).update({
            "profilePic": image_url
        })
        return {"message": "Profile picture updated", "url": image_url}, 200
    except Exception as e:
        print("Firestore update failed:", e)
        return {"message": "Failed to update Firestore"}, 500


# get first name
@setting_bp.route("/get-username")
def get_username():
    user_UID = request.args.get("userUID")
    if not user_UID:
        return jsonify({"message": "User UID required"}), 400

    try:
        doc = db.collection("users").document(user_UID).get()
        if doc.exists:
            return jsonify({"username": doc.to_dict().get("firstName")}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Error fetching username:", e)
        return jsonify({"message": "Server error"}), 500
    


@setting_bp.route("/get-profile-pic")
def get_profile_pic():
    user_UID = request.args.get("userUID") 
    if not user_UID:
        return jsonify({"message": "User UID required"}), 400

    try:
        doc = db.collection("users").document(user_UID).get()
        if doc.exists:
            return jsonify({"profilePic": doc.to_dict().get("profilePic")}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Error fetching profile picture:", e)
        return jsonify({"message": "Server error"}), 500

    
@setting_bp.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json()
    email = data.get("email")
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")

    try:
        user = pyrebase_auth.sign_in_with_email_and_password(email, old_password)

        id_token = user["idToken"]
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={os.environ.get('FIREBASE_API_KEY')}"

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
    
@setting_bp.route("/change-email", methods=["POST"])
def change_email():
    data = request.get_json()
    UID = data.get("userUID")
    new_email = data.get("newEmail")

    try:
        firebase_auth.update_user(UID, email=new_email)
        db.collection("users").document(UID).update({"email": new_email})
        users_ref = db.collection("usernames").where("userUID", "==", UID).stream()
        for doc_snapshot in users_ref:
            db.collection("usernames").document(doc_snapshot.id).update({"email": new_email})

        return jsonify({"message": "Email updated"}), 200
    except Exception as e:
        print("Email change failed:", e)
        return jsonify({"message": "Failed to update email"}), 500

@setting_bp.route("/change-username", methods=["POST"])
def change_username():
    data = request.get_json()
    UID = data.get("userUID")
    new_username = data.get("newUsername")

    if db.collection("usernames").document(new_username).get().exists:
        return jsonify({"message": "Username already exists"}), 400

    try:
        user_doc = db.collection("users").document(UID).get()
        if user_doc.exists:
            old_username = user_doc.to_dict().get("username")
            db.collection("usernames").document(old_username).delete()
            db.collection("usernames").document(new_username).set({
                "email": user_doc.to_dict().get("email"),
                "userUID": UID
            })
            db.collection("users").document(UID).update({"username": new_username})
            return jsonify({"message": "Username updated"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Username change failed:", e)
        return jsonify({"message": "Update failed"}), 500