from Entities import Settings
from Entities import Activity

class User:
    def __init__(self, uid=None, email=None, username=None, first_name=None, last_name=None,
                 settings=None, activities=None, saved_routes=None):
        self.__uid = uid
        self.__email = email
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__settings = settings
        self.__activites = activities
        self.__saved_routes = saved_routes
    
    def to_dict(self):
        return {
            "uid": self.__uid,
            "email": self.__email,
            "username": self.__username,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "settings": {} if self.__settings is None else self.__settings.to_dict(),
            "activities": [] if self.activities is None else [a.to_dict() for a in self.activities],
            "saved_routes": [] if self.saved_routes is None else [r.to_dict() for r in self.saved]
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            uid=data.get("uid") if "uid" in data else None,
            email=data.get("email") if "email" in data else None,
            username=data.get("username") if "username" in data else None,
            first_name=data.get("first_name") if "first_name" in data else None,
            last_name=data.get("last_name") if "last_name" in data else None,
            settings=Settings.from_dict(data.get("settings")) if "settings" in data else None,
            activities=[Activity.from_dict(a) for a in data.get("activities", [])],
            saved_routes=[SavedRoutes.from_dict(r) for r in data.get("saved_routes", [])]
        )
    
    # Getters and Setters
    
    # Getters
    def get_uid(self):
        return self.__uid
    
    def get_email(self):
        return self.__email
    
    def get_username(self):
        return self.__username
    
    def get_first_name(self):
        return self.__first_name
        
    def get_last_name(self):
        return self.__last_name

    def get_settings(self):
        return self.__settings
    
    def get_activities(self):
        return self.__activities
    
    def get_saved_routes(self):
        return self.__saved_routes


    # Setters
    def set_username(self, username):
        self.__username = username
        return self.__username
    
    def set_email(self, email):
        self.__email = email
        return self.__email
    
    def set_first_name(self, first_name):
        self.__first_name = first_name
        return self.__first_name
    
    def set_last_name(self, last_name):
        self.__last_name = last_name
        return self.__last_name
    
    def set_settings(self, settings):
        self.__settings = settings
        return self.__settings
    
    def set_activities(self, activities):
        self.__activities = activities
        return self.__activities
    
    def set_saved_routes(self, saved_routes):
        self.__saved_routes = saved_routes
        return self.__saved_routes