from flask import Blueprint,request,jsonify
from .services import db, firestore_module as firestore
from Controllers.ProfilePageController import ProfilePageController
from Controllers.SavedRoutesController import SavedRoutesController
import traceback


savedroutes_bp = Blueprint("savedroutes",__name__)

profile_controller = ProfilePageController()
saved_route_controller = SavedRoutesController()

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
        return saved_route_controller.unsave_route(user_uid, route_id)
    
    except Exception as e:
        print("Error unsaving route:", e)
        return jsonify({"message": "Failed to unsave route"}), 500

#get saved routes
@savedroutes_bp.route("/get-saved-routes", methods=["GET"])
def get_saved_routes():
    user_uid = request.args.get("userUID")
    try:
        return saved_route_controller.fetch_saved_routes(user_uid)

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
        return saved_route_controller.update_last_used(user_uid, route_id)
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

        return profile_controller.delete_activity(user_uid, activity_id)

    except Exception as e:
        print("Error deleting activity:", e)
        traceback.print_exc()
        return jsonify({"error": "Failed to delete activity"}), 500
