from flask import Blueprint,request, session
import os

from Controllers.LoginPageController import LoginPageController



login_bp = Blueprint("login",__name__)

login_controller = LoginPageController()
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')


@login_bp.route("/auth", methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get("login")
    password = data.get("password")
    print("trying login")
    return login_controller.login(session, login_input, password)
    
@login_bp.route("/logout", methods=["POST"])
def logout():
    return login_controller.logout(session)

@login_bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password") # TODO: Hash password before storing (frontend should do this)
    first_name = data.get("firstName", "")
    last_name = data.get("lastName", "")

    return login_controller.register(email, username, password, first_name, last_name)

@login_bp.route('/google-login')
def google_login():
    return login_controller.google_login(GOOGLE_CLIENT_ID)




@login_bp.route('/google-callback')
def google_callback():
    code = request.args.get('code')
    return login_controller.google_callback(session,
                                            code,
                                            os.environ.get('GOOGLE_CLIENT_ID'),
                                            os.environ.get('GOOGLE_CLIENT_SECRET'))