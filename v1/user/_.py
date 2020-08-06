import falcon

from v1.authentication import authenticate
from entity.user.user_repo import UserRepo
from entity.user.user_repo import IGNORE


NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 40
ABOUT_MIN_LENGTH = 1
ABOUT_MAX_LENGTH = 128
CONTACT_MIN_LENGTH = 5
CONTACT_MAX_LENGTH = 600


class _:

    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Max-Age', 86400)  # One day

        token = req.get_header('token')

        user = None

        if True or token != 'web':
            user = authenticate(req, resp)

            if not user:
                return

        req_user_id = req.get_param('id', 'self')

        user_repo = UserRepo()

        if req.req_user_id != 'self' and req_user_id != user.get_public_id():
            raw_req_user_id = bytes.fromhex(req_user_id)

            user = user_repo.find_user(raw_req_user_id)

        if not user:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.media = {'message': 'User not found.'}
            return

        resp.status = falcon.HTTP_OK
        resp.media = user.get_public_obj()

    def on_put(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        name = req.media.get('name') if 'name' in req.media else IGNORE
        about = req.media.get('about') if 'about' in req.media else IGNORE
        contact = req.media.get('contact') if 'contact' in req.media else IGNORE

        name = _.prepare_arg(name)
        about = _.prepare_arg(about)
        contact = _.prepare_arg(contact)

        if type(name) == str and (len(name) < NAME_MIN_LENGTH or len(name) > NAME_MAX_LENGTH):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.media = {'message': 'Invalid name length.'}
            return

        if type(about) == str and (len(about) < ABOUT_MIN_LENGTH or len(about) > ABOUT_MAX_LENGTH):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.media = {'message': 'Invalid about length.'}
            return

        if type(contact) == str and (len(contact) < CONTACT_MIN_LENGTH or len(contact) > CONTACT_MAX_LENGTH):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.media = {'message': 'Invalid contact length.'}
            return

        UserRepo.update_user(user, name, about, contact)

        resp.status = falcon.HTTP_ACCEPTED
        resp.media = user.get_public_obj()

    def prepare_arg(value):
        if value == IGNORE or value is None:
            return value

        s_value = str(value)

        if len(s_value) == 0:
            return None

        return s_value

    def on_options(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Max-Age', 86400)  # One day
        resp.media = {'message': 'OK'}


def setup(app, prefix):
    app.add_route(prefix, _())
