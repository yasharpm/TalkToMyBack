from entity.base_entity import BaseEntity
import ttm_util


class Token(BaseEntity):

    TOKEN_LIFE = 3 * ttm_util.ONE_DAY

    USER_ID = 'user_id'
    LIFE = 'life'

    def __init__(self, user_id=None, companion=None):
        if not companion:
            companion = {}

        if user_id:
            companion[Token.USER_ID] = user_id

        companion[Token.LIFE] = Token.TOKEN_LIFE

        BaseEntity.__init__(self, companion)

    def get_public_obj(self):
        obj = super(Token, self).get_public_obj()

        obj.pop(Token.USER_ID, None)

        return obj

    def get_life(self):
        return self.get_obj()[Token.LIFE]