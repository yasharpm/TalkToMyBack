import falcon

from entity.repositories import REFRESH_TOKEN_REPO
from entity.repositories import TOKEN_REPO
from entity.repositories import USER_REPO


class Register:

    def on_post(self, req, resp):
        raw_password = req.media.get('password')

        user = USER_REPO.new_user(raw_password)
        user_id = user.get_mongo_id()

        refresh_token = REFRESH_TOKEN_REPO.new_refresh_token(user)

        token = TOKEN_REPO.new_token(refresh_token)

        response = {
            'userId': user.get_public_id(),
            'token': token.get_public_id(),
            'refreshToken': refresh_token.get_public_id(),
            'tokenLife': token.get_life()
        }

        resp.status = falcon.HTTP_200
        resp.media = response


def setup(app, prefix):
    app.add_route(prefix + '/register', Register())
