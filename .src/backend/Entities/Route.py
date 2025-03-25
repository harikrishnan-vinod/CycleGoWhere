from Entities.Location import Location

class Route:
    def __init__(self, start_point=None, end_point=None, route_id=None, distance=0, 
                 estimated_time=0, route_path=None):
        self.__route_id = route_id
        self.__start_point = start_point
        self.__end_point = end_point
        self.__total_distance = distance  # in kilometers
        self.__total_time = estimated_time  # in seconds
        self.__route_path = route_path or {}  # list of Location objects representing the path
    
    def to_dict(self):
        return {
            "route_id": self.__route_id,
            "start_point": self.__start_point.to_dict() if self.__start_point else None,
            "end_point": self.__end_point.to_dict() if self.__end_point else None,
            "distance": self.__total_distance,
            "total_time": self.__total_time,
            "path": {location.to_dict() for location in self.__route_path} if self.__route_path else []
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
        return self.start_location
    
    def get_end_location(self):
        return self.end_location
    
    def get_distance(self):
        return self.distance
    
    def get_estimated_time(self):
        return self.estimated_time
    
    # Set methods
    def set_start_location(self, location):
        self.start_location = location
        return True
    
    def set_end_location(self, location):
        self.end_location = location
        return True
    
    def set_distance(self, distance):
        self.distance = distance
        return True
    
    def set_estimated_time(self, time):
        self.estimated_time = time
        return True