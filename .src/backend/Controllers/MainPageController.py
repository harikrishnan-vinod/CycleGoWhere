from flask import request, jsonify
from Entities.Route import Route
from Entities.Location import Location
from Entities.DatabaseController import DatabaseController

class MainPageController:
    def __init__(self):
        self.db_controller = DatabaseController()
    
    def search_route(self, from_location, to_location, user_id):
        try:
            # Process locations
            start = Location(from_location["name"], from_location["latitude"], from_location["longitude"])
            end = Location(to_location["name"], to_location["latitude"], to_location["longitude"])
            
            # Generate route using external API or algorithm
            # This would be replaced with actual API call
            route = Route(start, end)
            
            # Save to recent searches
            self.db_controller.add_recent_search(user_id, route)
            
            return route.to_dict()
        except Exception as e:
            return {"error": str(e)}, 400
    
    def filter_map(self, filter_options):
        try:
            # Query filtered facilities
            facilities = []
            
            if filter_options.get("water_coolers"):
                facilities.extend(self.db_controller.get_facilities("water_cooler"))
                
            if filter_options.get("bike_repair"):
                facilities.extend(self.db_controller.get_facilities("bike_repair"))
                
            if filter_options.get("bike_park"):
                facilities.extend(self.db_controller.get_facilities("bike_park"))
                
            return {"facilities": facilities}
        except Exception as e:
            return {"error": str(e)}, 400
    
    def navigate_route(self, route_id, user_id):
        try:
            route = self.db_controller.get_route(route_id)
            
            # Get facilities along route
            facilities = self.db_controller.get_facilities_along_route(route)
            
            # Check weather for route
            weather = self.check_weather(route)
            
            return {
                "route": route.to_dict(),
                "facilities": facilities,
                "weather": weather
            }
        except Exception as e:
            return {"error": str(e)}, 400
    
    def check_weather(self, route):
        # Mock weather API call
        # Would be replaced with actual weather API
        return {
            "condition": "clear",
            "temperature": 28,
            "uv_index": 6,
            "rain_probability": 10
        }