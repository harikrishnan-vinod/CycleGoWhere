class SavedRoutes:
    def __init__(self,
                 saved_route_id=None,
                 user_UID=None, distance=0,
                 end_location=None,
                 end_postal=None,
                 instructions=[],
                 last_used_at=None,
                 notes=None,
                 route_name=None,
                 route_path=[],
                 start_location=None,
                 start_postal=None,
                 ):
                 
        self.__saved_route_id = saved_route_id
        self.__user_UID = user_UID
        self.__distance = distance
        self.__end_location = end_location
        self.__end_postal = end_postal
        self.__instructions = instructions
        self.__last_used_at = last_used_at
        self.__notes = notes
        self.__route_name = route_name
        self.__route_path = route_path
        self.__start_location = start_location
        self.__start_postal = start_postal
        
    
    def to_dict(self):
        return {
            "user_uid": self.user_uid,
            "routes": [route.to_dict() for route in self.routes]
        }
    
    @staticmethod
    def from_dict(data, routes):
        saved_routes = SavedRoutes(
            user_uid=data.get("user_uid"),
            routes=routes
        )
        return saved_routes
    
    # Getters and Setters
    def get_saved_route_id(self):
        return self.__saved_route_id
    
    def get_user_UID(self):
        return self.__user_UID
    
    def get_distance(self):
        return self.__distance
    
    def get_end_location(self):
        return self.__end_location
    
    def get_end_postal(self):
        return self.__end_postal
    
    def get_instructions(self):
        return self.__instructions
    
    def get_last_used_at(self):
        return self.__last_used_at
    
    def get_notes(self):
        return self.__notes
    
    def get_route_name(self):
        return self.__route_name
    
    def get_route_path(self):
        return self.__route_path
    
    def get_start_location(self):
        return self.__start_location
    
    def get_start_postal(self):
        return self.__start_postal
    
    def set_saved_route_id(self, saved_route_id):
        self.__saved_route_id = saved_route_id
        return self.__saved_route_id
    
    def set_user_UID(self, user_UID):
        self.__user_UID = user_UID
        return self.__user_UID
    
    def set_distance(self, distance):
        self.__distance = distance
        return self.__distance
    
    def set_end_location(self, end_location):
        self.__end_location = end_location
        return self.__end_location
    
    def set_end_postal(self, end_postal):
        self.__end_postal = end_postal
        return self.__end_postal
    
    def set_instructions(self, instructions):
        self.__instructions = instructions
        return self.__instructions
    
    def set_last_used_at(self, last_used_at):
        self.__last_used_at = last_used_at
        return self.__last_used_at
    
    def set_notes(self, notes):
        self.__notes = notes
        return self.__notes
    
    def set_route_name(self, route_name):
        self.__route_name = route_name
        return self.__route_name
    
    def set_route_path(self, route_path):
        self.__route_path = route_path
        return self.__route_path
    
    def set_start_location(self, start_location):
        self.__start_location = start_location
        return self.__start_location
    
    def set_start_postal(self, start_postal):
        self.__start_postal = start_postal
        return self.__start_postal