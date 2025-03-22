from datetime import datetime

class Activity:
    """Represents a cycling activity session recorded by a user.
    
    Attributes:
        activity_id (int): Unique identifier for the activity
        user (User): User who performed the activity
        date_time_started (datetime): Activity start timestamp
        date_time_ended (datetime): Activity end timestamp
        time_elapsed (float): Total activity duration in seconds
        route_taken (Route): Cycling route used for this activity
        filters_used (Filters): Map filters applied during activity
    """

    def __init__(self, activity_id: int, user: 'User'):
        """Initializes a new Activity instance.
        
        Args:
            activity_id: Unique numeric identifier
            user: Associated User object
        """
        self.activity_id = activity_id
        self.user = user
        self.date_time_started = None
        self.date_time_ended = None
        self.time_elapsed = 0.0
        self.route_taken = None
        self.filters_used = None

    def set_route_taken(self, route: 'Route') -> bool:
        """Links a cycling route to this activity.
        
        Args:
            route: Route object representing path taken
            
        Returns:
            bool: True if successfully set
        """
        self.route_taken = route
        return True

    def get_time_elapsed(self) -> float:
        """Calculates duration between start and end times.
        
        Returns:
            float: Activity duration in seconds
        """
        if self.date_time_started and self.date_time_ended:
            return (self.date_time_ended - self.date_time_started).total_seconds()
        return 0.0