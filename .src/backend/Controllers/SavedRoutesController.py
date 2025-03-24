from flask import request, jsonify
from Entities.Route import Route
from Entities.SavedRoutes import SavedRoutes
from Entities.DatabaseController import DatabaseController

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
    
    def save_route(self, user_id, route_id):
        try:
            # Save route
            route = self.db_controller.get_route(route_id)
            self.db_controller.save_route(user_id, route)
            
            return {"message": "Route saved successfully"}
        except Exception as e:
            return {"error": str(e)}, 400
    
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