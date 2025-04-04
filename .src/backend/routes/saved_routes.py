import datetime
import traceback
from flask import Blueprint, app,request,jsonify
import polyline
from .services import db, firestore_module as firestore
import polyline
import datetime
from Controllers.ProfilePageController import ProfilePageController
from Controllers.SavedRoutesController import SavedRoutesController


savedroutes_bp = Blueprint("savedroutes",__name__)

profile_controller = ProfilePageController()
save_route_controller = SavedRoutesController()


@savedroutes_bp.route("/save-route", methods=["POST"])
def save_route():
    data = request.get_json()
    user_uid = data.get("userUID")
    route_data = data.get("routeData")
    return profile_controller.save_route(user_uid, route_data)
    
@savedroutes_bp.route("/get-saved-routes", methods=["GET"])
def get_saved_routes():
    user_uid = request.args.get("userUID")
    try:
        return save_route_controller.fetch_saved_routes(user_uid)

    except Exception as e:
        print("Error fetching routes:", e)
        return jsonify({"message": "Could not fetch saved routes"}), 500

@savedroutes_bp.route("/get-activities", methods=["GET"]) 
def get_activities():
    user_uid = request.args.get("userUID")
    try:
        return profile_controller.fetch_activies(user_uid)
    except Exception as e:
        print("Error getting activities:", e)
        return jsonify({"message": "Could not fetch activities"}), 500
    
@savedroutes_bp.route("/update-last-used", methods=["POST"])
def update_last_used():
    user_uid = request.args.get("userUID")
    route_id = request.args.get("routeId")
    try:
        route_ref = db.collection("users").document(user_uid).collection("savedRoutes").document(route_id)
        route_ref.update({"lastUsedAt": firestore.SERVER_TIMESTAMP})
        return jsonify({"message": "Last used updated"}), 200
    except Exception as e:
        print("Error updating last used:", e)
        return jsonify({"message": "Failed to update last used"}), 500