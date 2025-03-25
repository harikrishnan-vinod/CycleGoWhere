class Settings:
    def __init__(self, user=None, notification_enabled=True, profile_picture=None):
        self.__user = user
        self.__notification_enabled = notification_enabled
        self.__profile_picture = profile_picture
    
    def to_dict(self):
        return {
            "user": self.__user.to_dict() if self.__user else None,
            "notification_enabled": self.__notification_enabled,
            "profile_picture": self.__profile_picture
        }
    
    @staticmethod
    def from_dict(data):
        return Settings(
            user=data.from_dict(data.get("user")),
            notification_enabled=data.get("notification_enabled", True),
            profile_picture=data.get("profile_picture")
        )
    
    # Getters and Setters

    # Getters
    def get_notification_enabled(self):
        return self.__notification_enabled
    
    def get_profile_picture(self):
        return self.__profile_picture
    
    # Setters
    def set_notification_enabled(self, enabled):
        self.__notification_enabled = enabled
        return self.__notification_enabled
    
    def set_profile_picture(self, picture_url):
        self.__profile_picture = picture_url
        return self.__profile_picture
    
    # Methods
    def change_password(self, new_password):
        self.__user.set_password(new_password)
        return True
    
    def change_email(self, new_email):
        self.__user.set_email(new_email)
        return True
    
    def change_username(self, new_username):
        self.__user.set_username(new_username)
        return True
    
    def toggle_notifications(self):
        self.__notification_enabled = not self.__notification_enabled
        return self.__notification_enabled