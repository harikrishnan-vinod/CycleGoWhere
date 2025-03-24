from datetime import datetime

class Activity:
    def __init__(self, id=None, user_id=None, route=None, start_time=None, end_time=None, 
                 distance=0, duration=0, calories=0, avg_speed=0, max_speed=0, 
                 min_elevation=0, max_elevation=0, cadence=0):
        self.id = id
        self.user_id = user_id
        self.route = route
        self.start_time = start_time or datetime.now()
        self.end_time = end_time
        self.distance = distance  # in kilometers
        self.duration = duration  # in seconds
        self.calories = calories
        self.average_speed = avg_speed  # in km/h
        self.max_speed = max_speed  # in km/h
        self.min_elevation = min_elevation  # in meters
        self.max_elevation = max_elevation  # in meters
        self.cadence = cadence  # in rpm
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "route": self.route.to_dict() if self.route else None,
            "start_time": self.start_time.isoformat() if isinstance(self.start_time, datetime) else self.start_time,
            "end_time": self.end_time.isoformat() if isinstance(self.end_time, datetime) else self.end_time,
            "distance": self.distance,
            "duration": self.duration,
            "calories": self.calories,
            "average_speed": self.average_speed,
            "max_speed": self.max_speed,
            "min_elevation": self.min_elevation,
            "max_elevation": self.max_elevation,
            "cadence": self.cadence
        }
    
    @staticmethod
    def from_dict(data):
        activity = Activity(
            id=data.get("id"),
            user_id=data.get("user_id"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            distance=data.get("distance", 0),
            duration=data.get("duration", 0),
            calories=data.get("calories", 0),
            avg_speed=data.get("average_speed", 0),
            max_speed=data.get("max_speed", 0),
            min_elevation=data.get("min_elevation", 0),
            max_elevation=data.get("max_elevation", 0),
            cadence=data.get("cadence", 0)
        )
        return activity