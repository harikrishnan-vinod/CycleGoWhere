from datetime import datetime
from Entities.Route import Route

class Activity:
    def __init__(self, user_uid, activity_id=None, activity_name=None, notes=None,
                 duration=None, start_time=None, route: Route=None,
                 created_at=None):
        self.__user_uid = user_uid
        self.__activity_id = activity_id
        self.__activity_name = activity_name
        self.__notes = notes
        self.__duration = duration
        self.__start_time = start_time
        self.__route = route
        self.__created_at = created_at
        
    
    def to_dict(self):
        return {
            "user_uid": self.__user_uid,
            "activity_id": self.__activity_id,
            "activity_name": self.__activity_name,
            "notes": self.__notes,
            "duration": self.__duration,
            "start_time": self.__start_time,
            "route": self.__route.to_dict() if self.__route else None,
            "created_at": self.__created_at
        }
    
    @staticmethod
    def from_dict(data):
        activity = Activity(
            id=data.get("id"),
            user_uid=data.get("user_uid"),
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
    
    # Getters and Setters
    def get_user_uid(self):
        return self.__user_uid
    
    def get_activity_id(self):
        return self.__activity_id

    def get_activity_name(self):
        return self.__activity_name

    def get_notes(self):
        return self.__notes

    def get_duration(self):
        return self.__duration

    def get_start_time(self):
        return self.__start_time

    def get_instructions(self):
        return self.__instructions

    def get_route(self):
        return self.__route

    def get_created_at(self):
        return self.__created_at

    def set_user_uid(self, user_uid):
        self.__user_uid = user_uid
        return self.__user_uid

    def set_activity_name(self, activity_name):
        self.__activity_id = activity_name
        return self.__activity_id
    
    def set_activity_id(self, activity_id):
        self.__activity_id = activity_id
        return self.__activity_id

    def set_notes(self, notes):
        self.__notes = notes
        return self.__notes

    def set_distance(self, distance):
        self.__distance = distance
        return self.__distance

    def set_duration(self, duration):
        self.__duration = duration
        return self.__duration

    def set_start_time(self, start_time):
        self.__start_time = start_time
        return self.__start_time

    def set_instructions(self, instructions):
        self.__instructions = instructions
        return self.__instructions

    def set_route(self, route):
        self.__route = route
        return self.__route

    def set_created_at(self, created_at):
        self.__created_at = created_at
        return self.__created_at