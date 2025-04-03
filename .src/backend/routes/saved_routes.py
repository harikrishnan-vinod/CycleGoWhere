from flask import Blueprint,request,jsonify
import polyline
from .services import db, firestore_module as firestore


savedroutes_bp = Blueprint("savedroutes",__name__)



@savedroutes_bp.route("/save-route", methods=["POST"])
def save_route():
    data = request.get_json()
    user_uid = data.get("userUID")
    route_data = data.get("routeData")
    try:
        decoded_points = polyline.decode(route_data["route_geometry"], 5)
        geo_points = []
        for lat, lng in decoded_points:
            geo_points.append(firestore.GeoPoint(lat, lng))

        instructions_converted = []
        for row in route_data["route_instructions"]:
            instructions_converted.append({
                "direction": row[0],
                "road": row[1],
                "distance": row[5],
                "latLng": row[3]
            })

        doc_data = {
            "routeName": route_data["routeName"],
            "notes": route_data["notes"],
            "distance": route_data["distance"],
            "startPostal": route_data["startPostal"],
            "endPostal": route_data["endPostal"],
            "routePath": geo_points,
            "instructions": instructions_converted,
            "startLocation": firestore.GeoPoint(decoded_points[0][0], decoded_points[0][1]),
            "endLocation": firestore.GeoPoint(decoded_points[-1][0], decoded_points[-1][1]),
            "lastUsedAt": firestore.SERVER_TIMESTAMP
        }

        db.collection("users").document(user_uid).collection("savedRoutes").add(doc_data)
        return jsonify({"message": "Route saved successfully"}), 200
    except Exception as e:
        print("Error saving route:", e)
        return jsonify({"message": "Failed to save route"}), 500


@savedroutes_bp.route("/get-saved-routes", methods=["GET"])
def get_saved_routes():
    user_uid = request.args.get("userUID")
    try:
        routes_ref = db.collection("users").document(user_uid).collection("savedRoutes").stream()
        routes = [{**r.to_dict(), "id": r.id} for r in routes_ref]
        return jsonify(routes), 200
    except Exception as e:
        print("Error fetching routes:", e)
        return jsonify({"message": "Could not fetch saved routes"}), 500

@savedroutes_bp.route("/save-activity", methods=["POST"])
def save_activity():
    data = request.get_json()
    user_uid = data.get("userUID")
    activity_data = data.get("activityData")  # Should include route name, time taken, start/end points, notes, etc.

    try:
        activity_ref = db.collection("users").document(user_uid).collection("activities")
        activity_ref.add(activity_data)
        return jsonify({"message": "Activity saved"}), 200
    except Exception as e:
        print("Error saving activity:", e)
        return jsonify({"message": "Failed to save activity"}), 500


@savedroutes_bp.route("/get-activities", methods=["GET"])
def get_activities():
    user_uid = request.args.get("userUID")
    try:
        act_ref = db.collection("users").document(user_uid).collection("activities").stream()
        activities = [{**a.to_dict(), "id": a.id} for a in act_ref]
        return jsonify(activities), 200
    except Exception as e:
        print("Error getting activities:", e)
        return jsonify({"message": "Could not fetch activities"}), 500