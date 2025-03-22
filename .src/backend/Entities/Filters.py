class Filters:
    """Manages display filters for map features in the cycling application.
    
    Attributes:
        _show_water_point (bool): Visibility of water stations on map
        _show_repair_shop (bool): Visibility of bike repair shops on map
    """

    def __init__(self):
        """Initializes default filter settings"""
        self._show_water_point = False
        self._show_repair_shop = False

    def get_water_point(self) -> bool:
        """Retrieves water point display status.
        
        Returns:
            bool: True if water points are visible
        """
        return self._show_water_point

    def set_show_water_point(self, visible: bool) -> bool:
        """Updates water point visibility.
        
        Args:
            visible: New visibility state
            
        Returns:
            bool: True if update successful
        """
        self._show_water_point = visible
        return True

    def set_show_repair_shop(self, visible: bool) -> bool:
        """Updates repair shop visibility.
        
        Args:
            visible: New visibility state
            
        Returns:
            bool: True if update successful
        """
        self._show_repair_shop = visible
        return True