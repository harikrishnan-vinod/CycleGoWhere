from Entities.Location import Location

class Route:
    def __init__(self, start_location=None, end_location=None, id=None, distance=0, 
                 estimated_time=0, elevation_gain=0, path=None):
        self.id = id
        self.start_location = start_location
        self.end_location = end_location
        self.distance = distance  # in kilometers
        self.estimated_time = estimated_time  # in seconds
        self.elevation_gain = elevation_gain  # in meters
        self.path = path or []  # list of Location objects representing the path
    
    def to_dict(self):
        return {
            "id": self.id,
            "start_location": self.start_location.to_dict() if self.start_location else None,
            "end_location": self.end_location.to_dict() if self.end_location else None,
            "distance": self.distance,
            "estimated_time": self.estimated_time,
            "elevation_gain": self.elevation_gain,
            "path": [location.to_dict() for location in self.path] if self.path else []
        }
    
    @staticmethod
    def from_dict(data):
        start_location = None
        if data.get("start_location"):
            start_location = Location.from_dict(data["start_location"])
        
        end_location = None
        if data.get("end_location"):
            end_location = Location.from_dict(data["end_location"])
        
        path = []
        if data.get("path"):
            path = [Location.from_dict(loc) for loc in data["path"]]
        
        return Route(
            id=data.get("id"),
            start_location=start_location,
            end_location=end_location,
            distance=data.get("distance", 0),
            estimated_time=data.get("estimated_time", 0),
            elevation_gain=data.get("elevation_gain", 0),
            path=path
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