import falcon

import ttm_util
from entity.token.token_repo import TokenRepo
from entity.token.token import Token
from entity.user.user_repo import UserRepo


def authenticate(req, resp):
    token_id = req.get_header('token')

    if not token_id:
        resp.status = falcon.HTTP_400  # Bad request
        resp.media = {'message': "'token' not provided in header."}
        return None

    token = TokenRepo().authorize(token_id)

    if not token:
        resp.status = falcon.HTTP_401  # Unauthorized
        resp.media = {'message': 'Token not found.'}
        return None

    token_obj = token.get_obj()

    now = ttm_util.now()
    then = token_obj[Token.CREATED_TIME]

    if now - then > token.get_life() * 1000:
        resp.status = falcon.HTTP_401  # Unauthorized
        resp.media = {'message': 'Token is expired'}
        return None

    user_id = token_obj[Token.USER_ID]

    user = UserRepo().find_user(user_id)

    if not user:
        # Someone deleted the user from database without telling?!
        resp.status = falcon.HTTP_410  # Gone
        resp.media = {'message': 'User not exists. Should\'t really happen!'}
        return None

    # Further processing of user. For example maybe a deleted account? Can go here...

    return user
