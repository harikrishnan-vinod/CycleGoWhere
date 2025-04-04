from flask import Blueprint,request,jsonify
from .services import db, firestore_module as firestore
from Controllers.ProfilePageController import ProfilePageController

profile_bp = Blueprint("profile",__name__)
profile_controller = ProfilePageController()

@profile_bp.route("/get-username")
def get_username():
    user_UID = request.args.get("userUID")
    return profile_controller.get_username(user_UID)
    

@profile_bp.route("/get-profile-pic")
def get_profile_pic():
    user_UID = request.args.get("userUID")
    return profile_controller.get_profile_pic(user_UID)

@profile_bp.route("/get-activities", methods=["GET"])
def get_activities():
    user_uid = request.args.get("userUID")
    try:
        act_ref = db.collection("users").document(user_uid).collection("activities").stream()
        activities = []
        for doc in act_ref:
            data = doc.to_dict()
            data = to_serializable(data)
            data["id"] = doc.id
            print(doc.id)
            activities.append(data)
        return jsonify(activities), 200
    except Exception as e:
        print("Error getting activities:", e)
        return jsonify({"message": "Could not fetch activities"}), 500


def to_serializable(doc_dict):
    for key, value in doc_dict.items():
        if isinstance(value, firestore.GeoPoint):
            doc_dict[key] = {
                "latitude": value.latitude,
                "longitude": value.longitude
            }
        elif isinstance(value, dict):
            to_serializable(value)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], firestore.GeoPoint):
                    value[i] = {
                        "latitude": value[i].latitude,
                        "longitude": value[i].longitude
                    }
                elif isinstance(value[i], dict):
                    to_serializable(value[i])
    return doc_dict