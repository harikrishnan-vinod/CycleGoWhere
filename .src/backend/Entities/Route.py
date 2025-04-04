

class Route:
    def __init__(self,
                 route_id=None,
                 route_name=None,
                 notes=None,
                 start_location=None,
                 start_postal=None,
                 end_location=None,
                 end_postal=None,
                 distance=0,
                 route_path=[],
                 instructions=None,
                 last_used_at=None,):
        self.__start_location = start_location
        self.__start_postal = start_postal
        self.__end_location = end_location
        self.__end_postal = end_postal
        self.__distance = distance  # in kilometers
        self.__route_path = route_path or []  # list of Location objects representing the path
        self.__instructions = instructions
        self.__route_id = route_id
        self.__route_name = route_name
        self.__notes = notes
        self.__last_used_at = last_used_at

    def to_dict(self):
        return {
            "start_location": self.__start_location if self.__start_location else None,
            "start_postal": self.__start_postal,
            "end_location": self.__end_location if self.__end_location else None,
            "end_postal": self.__end_postal,
            "distance": self.__distance,
            "route_path": self.__route_path,
            "instructions": self.__instructions,
            "route_id": self.__route_id,
            "route_name": self.__route_name,
            "notes": self.__notes,
            "last_used_at": self.__last_used_at
        }
    
    @staticmethod
    def from_dict(data):
        start_location = None
        if data.get("start_location"):
            start_location = Location.from_dict(data["start_location"])
        
        end_location = None
        if data.get("end_location"):
            end_location = Location.from_dict(data["end_location"])
        
        route_path = {}
        if data.get("route_path"):
            route_path = dict([Location.from_dict(loc) for loc in data["route_path"]])
        
        return Route(
            id=data.get("id"),
            start_location=start_location,
            end_location=end_location,
            distance=data.get("distance", 0),
            estimated_time=data.get("estimated_time", 0),
            route_path=route_path
        )
    
    # Get methods
    def get_start_location(self):
        return self.__start_location

    def get_start_postal(self):
        return self.__start_postal

    def get_end_location(self):
        return self.__end_location

    def get_end_postal(self):
        return self.__end_postal

    def get_distance(self):
        return self.__distance

    def get_route_path(self):
        return self.__route_path

    def get_instructions(self):
        return self.__instructions
    
    def get_route_id(self):
        return self.__route_id
    
    def get_route_name(self):
        return self.__route_name
    
    def get_notes(self):
        return self.__notes
    
    def get_last_used_at(self):
        return self.__last_used_at

    def set_start_location(self, start_location):
        self.__start_location = start_location
        return self.__start_location

    def set_start_postal(self, start_postal):
        self.__start_postal = start_postal
        return self.__start_postal

    def set_end_location(self, end_location):
        self.__end_location = end_location
        return self.__end_location

    def set_end_postal(self, end_postal):
        self.__end_postal = end_postal
        return self.__end_postal

    def set_distance(self, distance):
        self.__distance = distance
        return self.__distance

    def set_route_path(self, route_path):
        self.__route_path = route_path
        return self.__route_path

    def set_instructions(self, instructions):
        self.__instructions = instructions
        return self.__instructions
    
    def set_route_id(self, route_id):
        self.__route_id = route_id
        return self.__route_id
    
    def set_route_name(self, route_name):
        self.__route_name = route_name
        return self.__route_name
    
    def set_notes(self, notes):
        self.__notes = notes
        return self.__notes
    
    def set_last_used_at(self, last_used_at):
        self.__last_used_at = last_used_at
        return self.__last_used_at

    