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

# save route
@savedroutes_bp.route("/save-route", methods=["POST"])
def save_route():
    data = request.get_json()
    user_uid = data.get("userUID")
    route_data = data.get("routeData")
    return profile_controller.save_route(user_uid, route_data)
#unsave route (in saved route page)
@savedroutes_bp.route("/unsave-route", methods=["DELETE"])
def unsave_route():
    data = request.get_json()
    user_uid = data.get("userUID")
    route_id = data.get("routeId")

    if not user_uid or not route_id:
        return jsonify({"message": "Missing userUID or routeId"}), 400

    try:
        db.collection("users").document(user_uid).collection("savedRoutes").document(route_id).delete()
        return jsonify({"message": "Route unsaved successfully"}), 200
    except Exception as e:
        print("Error unsaving route:", e)
        return jsonify({"message": "Failed to unsave route"}), 500

#get saved routes
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
    
@savedroutes_bp.route("/update-last-used", methods=["POST"]) #TODO: Use controller
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

#delete activity
@savedroutes_bp.route("/delete-activity", methods=["DELETE"])
def delete_activity():
    try:
        data = request.get_json()
        user_uid = data.get("userUID")
        activity_id = data.get("activityId")

        if not user_uid or not activity_id:
            return jsonify({"error": "Missing userUID or activityId"}), 400

        # Reference to the specific activity document
        activity_ref = db.collection("users").document(user_uid).collection("activities").document(activity_id)

        # Check if activity exists
        if not activity_ref.get().exists:
            return jsonify({"error": "Activity not found"}), 404

        # Delete the activity
        activity_ref.delete()

        return jsonify({"message": "Activity deleted successfully"}), 200

    except Exception as e:
        print("Error deleting activity:", e)
        traceback.print_exc()
        return jsonify({"error": "Failed to delete activity"}), 500
