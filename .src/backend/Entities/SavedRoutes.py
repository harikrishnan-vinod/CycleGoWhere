class SavedRoutes:
    def __init__(self, user_id=None, routes=None):
        self.user_id = user_id
        self.routes = routes or []  # list of Route objects
    
    def add_route(self, route):
        self.routes.append(route)
    
    def remove_route(self, route_id):
        self.routes = [route for route in self.routes if route.id != route_id]
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "routes": [route.to_dict() for route in self.routes]
        }
    
    @staticmethod
    def from_dict(data, routes):
        saved_routes = SavedRoutes(
            user_id=data.get("user_id"),
            routes=routes
        )
        return saved_routes