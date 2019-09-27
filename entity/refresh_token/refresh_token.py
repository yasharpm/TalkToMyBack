from entity.base_entity import BaseEntity


class RefreshToken(BaseEntity):

    USER_ID = 'user_id'
    USER_PUBLIC_ID = 'user_public_id'

    def __init__(self, user_id=None, user_public_id=None, companion=None):
        if not companion:
            companion = {}

        if user_id:
            companion[RefreshToken.USER_ID] = user_id

        if user_public_id:
            companion[RefreshToken.USER_PUBLIC_ID] = user_public_id

        BaseEntity.__init__(self, companion=companion)

    def get_public_obj(self):
        obj = super(RefreshToken, self).get_public_obj()

        obj.pop(RefreshToken.USER_ID, None)

        return obj
