from Location import Location

class Route:
    """Represents a cycling route between two locations.
    
    Attributes:
        start_point (Location): Route's starting location
        end_point (Location): Route's destination location
    """
    def __init__(self, start_point: Location, end_point: Location):
        """Initializes a new Route instance.
        
        Args:
            start_point: Location object for route start
            end_point: Location object for route end
        """
        self.start_point = start_point
        self.end_point = end_point

    # Getters
    def get_start_point(self) -> Location:
        return self.start_point

    def get_end_point(self) -> Location:
        return self.end_point

    # Setters
    def set_start_point(self, new_start: Location) -> bool:
        """Updates the route's starting location.
        
        Args:
            new_start: New Location object for start
            
        Returns:
            bool: True if update successful
        """
        self.start_point = new_start
        return True

    def set_end_point(self, new_end: Location) -> bool:
        self.end_point = new_end
        return True