from typing import List, Optional
from Entities import Settings
from Entities import Filters
from Entities import Activity
from Entities import SavedRoutes
from Entities import Route

class User:
    def __init__(self, id=None, email=None, username=None, profile_picture=None, 
                 notification_enabled=True, recent_searches=None):
        self.id = id
        self.email = email
        self.username = username
        self.profile_picture = profile_picture
        self.notification_enabled = notification_enabled
        self.recent_searches = recent_searches or []  # list of Route IDs
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "profile_picture": self.profile_picture,
            "notification_enabled": self.notification_enabled,
            "recent_searches": self.recent_searches
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            id=data.get("id"),
            email=data.get("email"),
            username=data.get("username"),
            profile_picture=data.get("profile_picture"),
            notification_enabled=data.get("notification_enabled", True),
            recent_searches=data.get("recent_searches", [])
        )