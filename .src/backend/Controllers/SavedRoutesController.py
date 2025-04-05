from flask import jsonify
from Entities.DatabaseController import DatabaseController, to_serializable
from routes.services import db, firestore_module as firestore
import polyline

class SavedRoutesController:
    def __init__(self):
        self.db_controller = DatabaseController()
    
    def fetch_saved_routes(self, user_uid):
        routes_data = []
        routes = self.db_controller.get_saved_routes(user_uid)
        for route in routes:
            route_dict = route.to_dict()
            raw_data = {
                "routeName": route_dict.get("route_name"),
                "notes": route_dict.get("notes"),
                "distance": route_dict.get("distance"),
                "startLocation": route_dict.get("start_location"),
                "startPostal": route_dict.get("start_postal"),
                "endLocation": route_dict.get("end_location"),
                "endPostal": route_dict.get("end_postal"),
                "routePath": route_dict.get("route_path"),
                "instructions": route_dict.get("instructions"),
                "lastUsedAt": route_dict.get("last_used_at"),
                "routeId": route_dict.get("route_id")
            }
            serializable_data = to_serializable(raw_data)

            route_path = serializable_data.get("routePath", [])
            if route_path and isinstance(route_path, list):
                try:
                    latlngs = [
                        (pt["latitude"], pt["longitude"]) for pt in route_path
                    ]
                    encoded = polyline.encode(latlngs, 5)
                    serializable_data["route_geometry"] = encoded
                except Exception as e:
                    print("⚠️ Failed to encode polyline:", e)
                    serializable_data["route_geometry"] = None

            serializable_data["id"] = route.get_route_id()
            routes_data.append(serializable_data)

        return jsonify(routes_data), 200
    
    def unsave_route(self, user_uid, route_id):
        try:
            # Unsave route
            self.db_controller.unsave_route(user_uid, route_id)
            return jsonify({"message": "Route unsaved successfully"}), 200
        except Exception as e:
            return jsonify({"message": "Failed to unsave route"}), 500
    
    def start_activity_from_saved(self, user_uid, route_id):
        try:
            # Get route
            route = self.db_controller.get_route(route_id)
            
            # Start navigation
            return {
                "route": route.to_dict(),
                "message": "Navigation started"
            }
        except Exception as e:
            return {"error": str(e)}, 400
        
    def unsave_activity(self, user_uid, route_id):
        try:
            self.db_controller.unsave_route(user_uid, route_id)
            return {"message": "Route unsaved successfully"}
        except Exception as e:
            return {"error": str(e)}, 400

    def update_last_used(self, user_uid, route_id):
        try:
            # Update last used timestamp
            if self.db_controller.update_last_used(user_uid, route_id):
                return jsonify({"message": "Last used updated"}), 200
        except Exception as e:
            return jsonify({"message": "Failed to update last used"}), 500