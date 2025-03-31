from Entities.User import User
from Entities.Settings import Settings
# from Entities.Activity import Activity
from flask import session

class SessionController:

    @staticmethod
    def set_user_session(user):
        if user.get_uid() not in session:
            session[user.get_uid()] = {}
            
        session[user.get_uid()]['email'] = user.get_email()
        session[user.get_uid()]['username'] = user.get_username()
        session[user.get_uid()]['settings'] = user.get_settings().to_dict()
        # TODO: Implement methods to get activities and saved routes from the database
        # session[user.uid]['activities'] = [a.to_dict() for a in user.get_activities()]
        # session[user.uid]['saved_routes'] = [r.to_dict() for r in user.get_saved_routes()]

    @staticmethod
    def get_user_session_from_uid(uid):
        if uid not in session:
            return None
        return User(uid,
                    session[uid]['email'],
                    session[uid]['username'],
                    Settings.from_dict(session[uid]['settings']),
                    # TODO: Implement logic to pass in activities and saved routes
                    # [Activity.from_dict(a) for a in session[uid]['activities']],
                    # [SavedRoutes.from_dict(r) for r in session[uid]['saved_routes']]
                    )

