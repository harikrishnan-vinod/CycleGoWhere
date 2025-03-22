class Settings:
    """Manages user preferences and account configuration.
    
    Attributes:
        _app_notifications (bool): Notification enablement status
        _user_id (str): Unique user identifier
        _password (str): Encrypted user password
        _email (str): User's email address
        _profile_picture (bytes): JPEG image data
    """

    def __init__(self):
        """Initializes default settings"""
        self._app_notifications = True
        self._user_id = ""
        self._password = ""
        self._email = ""
        self._profile_picture = b''

    def set_user_id(self, user_id: str) -> bool:
        """Updates user identifier.
        
        Args:
            user_id: New unique ID
            
        Returns:
            bool: True if update successful
        """
        self._user_id = user_id
        return True

    def set_app_notifications(self, enabled: bool) -> bool:
        """Configures application notifications.
        
        Args:
            enabled: True to enable notifications
            
        Returns:
            bool: True if update successful
        """
        self._app_notifications = enabled
        return True

    def set_profile_picture(self, image_data: bytes) -> bool:
        """Updates user profile picture.
        
        Args:
            image_data: JPEG image bytes
            
        Returns:
            bool: True if image accepted
        """
        self._profile_picture = image_data
        return True