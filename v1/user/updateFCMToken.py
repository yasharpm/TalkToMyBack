import falcon

from v1.authentication import authenticate
from entity.repositories import USER_REPO


class UpdateFCMToken:

    def on_post(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        token = req.media.get('token')

        if not token:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Token is not given.'}
            return

        USER_REPO.set_fcm_token(user, token)

        resp.status = falcon.HTTP_200
        resp.media = {'message': 'Success!'}


def setup(app, prefix):
    app.add_route(prefix + '/updateFCMToken', UpdateFCMToken())
