import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin._messaging_utils import UnregisteredError
from threading import Thread
import json

from entity.user.user import User


def init():
    #  cred = credentials.Certificate("/home/opentalkz/api/opentalkz-firebase-adminsdk.json")
    #  firebase_admin.initialize_app(cred)
    pass  # TODO


def _send_message(message):
    try:
        messaging.send(message)
    except UnregisteredError:
        pass


def send_notification(user, sync):
    if not user:
        return

    fcm_token = user.get_obj()[User.FCM_TOKEN]

    if not fcm_token:
        return

    data = {'sync': json.dumps(sync.get_public_obj())}

    # notification = messaging.Notification(title='salam', body='this is the body', image=None)
    message = messaging.Message(data=data, token=fcm_token)

    Thread(target=_send_message, args=(message, )).start()
