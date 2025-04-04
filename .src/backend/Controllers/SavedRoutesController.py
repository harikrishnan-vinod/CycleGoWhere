from flask import request, jsonify
from Entities.Route import Route
from Entities.SavedRoutes import SavedRoutes
from Entities.DatabaseController import DatabaseController
from flask import Blueprint, request, josonify
from routes.services import db, firestore_module as firestore
import polyline
import datetime
import traceback

class SavedRoutesController:
    def __init__(self):
        self.db_controller = DatabaseController()
    
    def get_saved_routes(self, user_id):
        try:
            # Get saved routes
            saved_routes = self.db_controller.get_saved_routes(user_id)
            
            return {
                "saved_routes": [route.to_dict() for route in saved_routes]
            }
        except Exception as e:
            return {"error": str(e)}, 400
    
    def save_route(self, user_id, route_data):
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
    
    def unsave_route(self, user_id, route_id):
        try:
            # Unsave route
            self.db_controller.unsave_route(user_id, route_id)
            
            return {"message": "Route unsaved successfully"}
        except Exception as e:
            return {"error": str(e)}, 400
    
    def start_activity_from_saved(self, user_id, route_id):
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