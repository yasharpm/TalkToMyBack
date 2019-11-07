import firebase_admin
from firebase_admin import credentials


def start():
    cred = credentials.Certificate("/home/talktome/talk-to-me-37911-firebase-adminsdk.json")
    app = firebase_admin.initialize_app(cred)

    print(app.name)
