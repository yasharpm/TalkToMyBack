import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import json

from entity.user.user import User


def init():
    cred = credentials.Certificate("/home/talktome/talk-to-me-37911-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)


def send_notification(user, sync):
    fcm_token = user.get_obj()[User.FCM_TOKEN]

    if not fcm_token:
        return

    data = {'sync': json.dumps(sync.get_public_obj())}

    notification = messaging.Notification(title='salam', body='this is the body', image=None)
    message = messaging.Message(data=data, token=fcm_token, notification=notification)
    response = messaging.send(message)

