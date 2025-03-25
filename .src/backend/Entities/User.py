from typing import List, Optional
from Entities import Settings
from Entities import Filters
from Entities import Activity
from Entities import SavedRoutes
from Entities import Route

class User:
    def __init__(self, uid=None, email=None, username=None, 
                 settings=None, activities=None):
        self.__uid = uid
        self.__email = email
        self.__username = username
        self.__setings = settings
        self.__activites = activities
    
    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "username": self.username,
            "settings": {} if self.settings is None else self.settings.to_dict(),
            "activities": [] if self.activities is None else [a.to_dict() for a in self.activities]
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            uid=data.get("uid"),
            email=data.get("email"),
            username=data.get("username"),
            settings=Settings.from_dict(data.get("settings")),
            activities=[Activity.from_dict(a) for a in data.get("activities", [])]
        )
    
    # Getters and Setters
    get_uid = lambda self: self.__uid
    get_email = lambda self: self.__email
    get_username = lambda self: self.__username
    get_settings = lambda self: self.__settings
    get_activities = lambda self: self.__activities

    set_username = lambda self, username: setattr(self, "__username", username)
    set_email = lambda self, email: setattr(self, "__email", email)
    set_settings = lambda self, settings: setattr(self, "__settings", settings)
    set_activities = lambda self, activities: setattr(self, "__activities", activities)