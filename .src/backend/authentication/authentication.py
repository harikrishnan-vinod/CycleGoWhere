import pyrebase

config = {
    "apiKey": "REMOVED",
  "authDomain": "REMOVED.firebaseapp.com",
  "projectId": "REMOVED",
  "storageBucket": "REMOVED",
  "messagingSenderId": "REMOVED",
  "appId": "1:REMOVED:web:496edabac517dfff8e3062",
  "databaseURL" :""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = 'test@gmail.com'
password = '123456'

user = auth.sign_in_with_email_and_password(email, password)
print(user)

info = auth.get_account_info(user['idToken'])
print(info)