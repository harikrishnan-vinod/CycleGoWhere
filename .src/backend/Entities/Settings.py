class Settings:
    def __init__(self, user_id=None, notification_enabled=True, theme="light"):
        self.user_id = user_id
        self.notification_enabled = notification_enabled
        self.theme = theme
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "notification_enabled": self.notification_enabled,
            "theme": self.theme
        }
    
    @staticmethod
    def from_dict(data):
        return Settings(
            user_id=data.get("user_id"),
            notification_enabled=data.get("notification_enabled", True),
            theme=data.get("theme", "light")
        )