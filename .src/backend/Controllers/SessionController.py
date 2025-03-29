class SessionController:

    @staticmethod
    def set_user(email):
        session["user"] = email

    @staticmethod
    def get_user():
        return session.get("user")

