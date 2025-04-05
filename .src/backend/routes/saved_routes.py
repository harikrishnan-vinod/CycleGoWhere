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

    if not isinstance(route_data["route_geometry"], str):
        raise ValueError("route_geometry must be an encoded polyline string.")

    try:
        decoded_points = polyline.decode(route_data["route_geometry"], 5)
        print("Received encoded polyline:", route_data["route_geometry"])

        
        if not decoded_points:
            raise ValueError("Polyline decoding returned empty list.")

        geo_points = [firestore.GeoPoint(lat, lng) for lat, lng in decoded_points]

        instructions_converted = []
        for row in route_data["route_instructions"]:
            if isinstance(row, dict):  
                instructions_converted.append({
                    "direction": row.get("direction"),
                    "road": row.get("road"),
                    "distance": row.get("distance"),
                    "latLng": row.get("latLng"),
                })
            elif isinstance(row, list):  
                instructions_converted.append({
                    "direction": row[0],
                    "road": row[1],
                    "distance": row[5],
                    "latLng": row[3],
            })



        doc_data = {
            "routeName": route_data["routeName"],
            "notes": route_data["notes"],
            "distance": route_data["distance"],
            "startPostal": route_data["startPostal"],
            "endPostal": route_data["endPostal"],
            "routePath": geo_points,
            "instructions": instructions_converted,
            "startLocation": firestore.GeoPoint(*decoded_points[0]),
            "endLocation": firestore.GeoPoint(*decoded_points[-1]),
            "lastUsedAt": firestore.SERVER_TIMESTAMP
        }

        db.collection("users").document(user_uid).collection("savedRoutes").add(doc_data)
        return jsonify({"message": "Route saved successfully"}), 200

    except Exception as e:
        print("Error saving route:", e)
        traceback.print_exc()
        return jsonify({"message": "Failed to save route"}), 500
    
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
