class Location:
    """Represents a geographic location with coordinates.
    
    Attributes:
        location_id (int): Unique location identifier
        latitude (float): Latitude coordinate in decimal degrees
        longitude (float): Longitude coordinate in decimal degrees
        address (str): Human-readable street address
    """
    def __init__(self, location_id: int, lat: float, lng: float, address: str):
        """Initializes a new Location instance.
        
        Args:
            location_id: Unique numeric identifier
            lat: Latitude value between -90 and 90
            lng: Longitude value between -180 and 180
            address: Physical street address
        """
        self.location_id = location_id
        self.latitude = lat
        self.longitude = lng
        self.address = address

    # Getters
    def get_location_id(self) -> int:
        return self.location_id

    def get_location_latitude(self) -> float:
        return self.latitude

    def get_location_longitude(self) -> float:
        return self.longitude

    def get_location_address(self) -> str:
        return self.address

    # Setters
    def set_location_id(self, new_id: int) -> bool:
        self.location_id = new_id
        return True

    def set_location_latitude(self, lat: float) -> bool:
        """Updates the latitude coordinate.
        
        Args:
            lat: New latitude value
            
        Returns:
            bool: Always returns True
        """
        self.latitude = lat
        return True

    def set_location_longitude(self, lng: float) -> bool:
        self.longitude = lng
        return True

    def set_location_address(self, address: str) -> bool:
        self.address = address
        return True