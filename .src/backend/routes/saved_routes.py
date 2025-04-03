import traceback
from flask import Blueprint, app,request,jsonify
import polyline
from .services import db, firestore_module as firestore


savedroutes_bp = Blueprint("savedroutes",__name__)


@savedroutes_bp.route("/save-route", methods=["POST"])
def save_route():
    data = request.get_json()
    user_uid = data.get("userUID")
    route_data = data.get("routeData")

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
    activity_data = data.get("activityData")
    start_time_str = activity_data.get("startTime")
    start_time = None
    if start_time_str:
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except Exception as e:
            print("Invalid startTime format:", e)
    try:
        decoded_points = polyline.decode(activity_data["route_geometry"], 5)
        geo_points = []
        for lat, lng in decoded_points:
            geo_points.append(firestore.GeoPoint(lat, lng))

        instructions_converted = []
        for row in activity_data["route_instructions"]:
            instructions_converted.append({
                "direction": row[0],
                "road": row[1],
                "distance": row[5],
                "latLng": row[3]
            })

        doc_data = {
            "activityName": activity_data["activityName"],
            "notes": activity_data["notes"],
            "distance": activity_data["distance"],
            "startPostal": activity_data["startPostal"],
            "endPostal": activity_data["endPostal"],
            "duration": activity_data["timeTaken"],
            "routePath": geo_points,
            "startTime": start_time,
            "instructions": instructions_converted,
            "startLocation": firestore.GeoPoint(decoded_points[0][0], decoded_points[0][1]),
            "endLocation": firestore.GeoPoint(decoded_points[-1][0], decoded_points[-1][1]),
            "createdAt": firestore.SERVER_TIMESTAMP
        }
        db.collection("users").document(user_uid).collection("activities").add(doc_data)
        return jsonify({"message": "Activity saved"}), 200
    except Exception as e:
        print("Error saving activity:", e)
        return jsonify({"message": "Failed to save activity"}), 500
    

@savedroutes_bp.route("/get-activities", methods=["GET"])  
def get_activities():
    user_uid = request.args.get("userUID")
    try:
        act_ref = db.collection("users").document(user_uid).collection("activities").stream()
        activities = []
        for doc in act_ref:
            data = doc.to_dict()
            data = to_serializable(data)
            data["id"] = doc.id
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