class SavedRoutes:
    """Represents a frequently used route saved by users.
    
    Attributes:
        route_name (str): User-defined route identifier
        distance (float): Total route distance in kilometers
        average_time_taken (int): Typical duration in seconds
        number_of_rides (int): Total times route was used
    """

    def __init__(self, route_name: str, distance: float):
        """Initializes a new SavedRoutes instance.
        
        Args:
            route_name: Descriptive name for route
            distance: Route length in kilometers
        """
        self.route_name = route_name
        self.distance = distance
        self.average_time_taken = 0
        self.number_of_rides = 0

    def update_average_time(self, new_time: int) -> bool:
        """Recalculates average duration after new ride.
        
        Args:
            new_time: Duration of latest ride in seconds
            
        Returns:
            bool: True if update successful
        """
        total = self.average_time_taken * self.number_of_rides
        self.number_of_rides += 1
        self.average_time_taken = (total + new_time) // self.number_of_rides
        return True