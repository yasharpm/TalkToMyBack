from entity.base_repo import BaseRepo
from entity.token.token import Token
from entity.refresh_token.refresh_token import RefreshToken


class TokenRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, 'token')

    def new_token(self, refresh_token):
        token = Token(user_id=refresh_token.get_obj()[RefreshToken.USER_ID])

        result = self.db.insert_one(token.get_obj())

        token.set_mongo_id(result.inserted_id)

        return token

    def authorize(self, public_id):
        real_id = bytes.fromhex(public_id)

        companion = self.db.find_one({RefreshToken.ID: real_id})

        if companion:
            return Token(companion=companion)

        return None
