from flask import request, jsonify
from Entities.Activity import Activity
from Entities.Route import Route
from Entities.DatabaseController import DatabaseController, to_serializable
from routes.services import db, firestore_module as firestore
import polyline
import traceback

class ProfilePageController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def fetch_activies(self, user_UID):
        activity_data = []
        activities = self.db_controller.get_user_activities(user_UID)
        for activity in activities:
            # activity_dict = activity.to_dict()
            data = {
                "id": activity.get_activity_id(),
                "activityName": activity.get_activity_name(),
                "notes": activity.get_notes(),
                "duration": activity.get_duration(),
                "startTime": activity.get_start_time(),
                "startLocation": activity.get_route().get_start_location(),
                "startPostal": activity.get_route().get_start_postal(),
                "endLocation": activity.get_route().get_end_location(),
                "endPostal": activity.get_route().get_end_postal(),
                "distance": activity.get_route().get_distance(),
                "routePath": activity.get_route().get_route_path(),
                "instructions": activity.get_route().get_instructions(),
                "createdAt": activity.get_created_at()
            }
            data = to_serializable(data)
            activity_data.append(data)
        return jsonify(activity_data), 200
    
    def delete_activity(self, user_UID, activity_id):
        try:

            if self.db_controller.delete_activity(user_UID, activity_id):
                return jsonify({"message": "Activity deleted successfully"}), 200
        except Exception as e:
            print("Error deleting activity:", e)
            return jsonify({"message": "Failed to delete activity"}), 500
    
    def save_route(self, user_UID, route_data):
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

            route = Route(route_name=route_data["routeName"],
                          notes=route_data["notes"],
                          distance=route_data["distance"],
                          start_postal=route_data["startPostal"],
                          end_postal=route_data["endPostal"],
                          route_path=geo_points,
                          instructions=instructions_converted,
                          start_location=firestore.GeoPoint(*decoded_points[0]),
                          end_location=firestore.GeoPoint(*decoded_points[-1]),
                          last_used_at=firestore.SERVER_TIMESTAMP)

            self.db_controller.save_route(user_UID, route)
            return jsonify({"message": "Route saved successfully"}), 200

        except Exception as e:
            print("Error saving route:", e)
            traceback.print_exc()
            return jsonify({"message": "Failed to save route"}), 500

    def get_username(self, user_UID):
        if not user_UID:
            return jsonify({"message": "User UID required"}), 400

        try:
            username = self.db_controller.get_username_by_uid(user_UID)
            if username:
                return jsonify({"username": username}), 200
            else:
                return jsonify({"message": "Username not found"}), 404
        except Exception as e:
            print("Error fetching username:", e)
            return jsonify({"message": "Server error"}), 500
        
    def get_profile_pic(self, user_UID):
        if not user_UID:
            return jsonify({"message": "User UID required"}), 400

        try:
            profile_pic = self.db_controller.get_profile_picture(user_UID)
            if not profile_pic == '':
                return jsonify({"profilePic": profile_pic}), 200
            else:
                return jsonify({"message": "Profile picture not found"}), 404
        except Exception as e:
            print("Error fetching profile picture:", e)
            return jsonify({"message": "Server error"}), 500
    
    def get_recent_activities(self, user_uid, limit=3):
        try:
            # Get recent activities
            activities = self.db_controller.get_user_activities(user_uid, limit=limit)
            
            return {
                "activities": [activity.to_dict() for activity in activities]
            }
        except Exception as e:
            return {"error": str(e)}, 400
    
    def get_all_ride_history(self, user_uid):
        try:
            # Get all activities
            activities = self.db_controller.get_user_activities(user_uid)
            
            return {
                "activities": [activity.to_dict() for activity in activities]
            }
        except Exception as e:
            return {"error": str(e)}, 400
    
    def delete_ride_history(self, user_uid, activity_id):
        try:
            # Delete activity
            self.db_controller.delete_activity(user_uid, activity_id)
            
            return {"message": "Activity deleted successfully"}
        except Exception as e:
            return {"error": str(e)}, 400