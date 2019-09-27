import falcon

from entity.user.user_repo import UserRepo
from entity.refresh_token.refresh_token_repo import RefreshTokenRepo
from entity.token.token_repo import TokenRepo


class Register:

    def on_post(self, req, resp):
        raw_password = req.media.get('password')

        user_repo = UserRepo()
        user = user_repo.new_user(raw_password)
        user_id = user.get_mongo_id()

        refresh_token_repo = RefreshTokenRepo()
        refresh_token = refresh_token_repo.new_refresh_token(user)

        token_repo = TokenRepo()
        token = token_repo.new_token(refresh_token)

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
