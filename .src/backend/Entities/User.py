from typing import List, Optional
from Entities import Settings
from Entities import Filters
from Entities import Activity
from Entities import SavedRoutes
from Entities import Route

class User:
    def __init__(self, uid=None, email=None, username=None, 
                 settings=None, activities=None, saved_routes=None, logged_in=False):
        self.__uid = uid # TODO: Might not be necessary, remove?
        self.__email = email
        self.__username = username
        self.__setings = settings
        self.__activites = activities
        self.__saved_routes = saved_routes
        self.__logged_in = logged_in
    
    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "username": self.username,
            "settings": {} if self.settings is None else self.settings.to_dict(),
            "activities": [] if self.activities is None else [a.to_dict() for a in self.activities],
            "saved_routes": [] if self.saved_routes is None else [r.to_dict() for r in self.saved]
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            uid=data.get("uid"),
            email=data.get("email"),
            username=data.get("username"),
            settings=Settings.from_dict(data.get("settings")),
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
    
    def set_settings(self, settings):
        self.__settings = settings
        return self.__settings
    
    def set_activities(self, activities):
        self.__activities = activities
        return self.__activities
    
    def set_saved_routes(self, saved_routes):
        self.__saved_routes = saved_routes
        return self.__saved_routes