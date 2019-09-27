from entity.base_repo import BaseRepo
from entity.refresh_token.refresh_token import RefreshToken


class RefreshTokenRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, 'refresh_token')

    def new_refresh_token(self, user):
        refresh_token = RefreshToken(user_id=user.get_mongo_id(), user_public_id=user.get_public_id())

        result = self.db.insert_one(refresh_token.get_obj())

        refresh_token.set_mongo_id(result.inserted_id)

        return refresh_token

    def find(self, public_id):
        real_id = bytes.fromhex(public_id)

        companion = self.db.find_one({RefreshToken.ID: real_id})

        if companion:
            return RefreshToken(companion=companion)

        return None
