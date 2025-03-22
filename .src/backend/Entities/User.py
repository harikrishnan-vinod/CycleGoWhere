from typing import List, Optional
from Entities import Settings
from Entities import Filters
from Entities import Activity
from Entities import SavedRoutes
from Entities import Route

class User:
    def __init__(
            self, 
            user_id: str, 
            email: str, 
            password: str,
            saved_routes: Optional[List[SavedRoutes]] = None,
            settings: Optional[Settings] = None,
            filters: Optional[Filters] = None,
            activities: Optional[List[Activity]] = None,
            ride_history: Optional[List[Activity]] = None, # TODO: Isn't ride_history the same as activities?
            personal_best: Optional[Activity] = None,
            profile_picture: Optional[bytes] = None # TODO: Save profile picture as bytes, or as a file path? Should be in Settings
    ):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.saved_routes = saved_routes if saved_routes is not None else []
        self.settings = settings if settings is not None else Settings()
        self.filters = filters if filters is not None else Filters()
        self.activities = activities if activities is not None else []
        self.ride_history = ride_history if ride_history is not None else []
        self.personal_best = personal_best if personal_best is not None else {}
        # TODO: self.profile_picture = profile

    # Getters
    def get_user_id(self) -> str:
        return self.user_id

    def get_email(self) -> str:
        return self.email

    def get_saved_routes(self) -> list:
        return self.saved_routes

    def get_recent_activity(self) -> dict:
        return self.activities[-1] if self.activities else {}

    def get_ride_history(self) -> list:
        return [activity for activity in self.activities]

    def get_personal_best(self) -> dict:
        return max(self.activities, key=lambda x: x['distance']) if self.activities else {}

    # Setters/Modifiers
    def add_saved_route(self, route: Route) -> bool:
        self.saved_routes.append(route)
        return True
    
    def add_activity(self, activity: Activity) -> bool:
        self.activities.append(activity)
        return True

    def set_personal_best(self, data: dict) -> bool:
        self.personal_best = data
        return True