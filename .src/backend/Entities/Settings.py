class Settings:
    def __init__(self, user=None, notification_enabled=True, profile_picture=None):
        self.__user = user
        self.__notification_enabled = notification_enabled
        self.__profile_picture = profile_picture
    
    def to_dict(self):
        return {
            "user": self.__user.to_dict() if self.__user else None,
            "notification_enabled": self.notification_enabled,
            "profile_picture": self.__profile_picture
        }
    
    @staticmethod
    def from_dict(data):
        return Settings(
            user_id=data.get("user_id"),
            notification_enabled=data.get("notification_enabled", True),
            profile_picture=data.get("theme", "light")
        )
    
    # Getters and Setters
    get_user = lambda self: self.__user
    get_notification_enabled = lambda self: self.__notification_enabled
    get_profile_picture = lambda self: self.__profile_picture

    set_user = lambda self, user: setattr(self, "__user", user)