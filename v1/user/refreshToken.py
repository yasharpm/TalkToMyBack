import falcon

from entity.refresh_token.refresh_token_repo import RefreshTokenRepo
import entity.refresh_token.refresh_token
from entity.token.token_repo import TokenRepo


class refreshToken:

    def on_post(self, req, resp):
        user_id = req.media.get('userId')
        refresh_token_id = req.media.get('refreshToken')

        if not user_id or not refresh_token_id:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': "'userId' or 'refreshToken' not provided."}
            return

        refresh_token_repo = RefreshTokenRepo()
        refresh_token = refresh_token_repo.find(refresh_token_id)

        # Is the refresh token valid?
        if refresh_token:
            token_user_public_id =\
                refresh_token.get_obj().get(entity.refresh_token.refresh_token.RefreshToken.USER_PUBLIC_ID)

            # Validate with user id (security measure)
            if token_user_public_id == user_id:
                token = TokenRepo().new_token(refresh_token)

                # Token is good to go
                resp.status = falcon.HTTP_200
                resp.media = {'token': token.get_public_id(), 'tokenLife': token.get_life()}
            else:
                # We have a hacker on our hands
                resp.status = falcon.HTTP_417  # Expectation failed
                resp.media = {'token': 'Is it a F*ing hackaton? Or are you just another a*hole?', 'tokenLife': 0}
        else:
            # Invalid refresh token id. Probably token removed.
            resp.status = falcon.HTTP_401  # Unauthorized
            resp.media = {'message': 'Refresh token does not exist.'}


def setup(app, prefix):
    app.add_route(prefix + '/refreshToken', refreshToken())
