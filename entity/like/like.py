import ttm_util


class Like:

    CREATED_TIME = 'created_time'

    USER_ID = 'user_id'
    POST_ID = 'post_id'

    def __init__(self, user_id=None, post_id=None, companion=None):
        if not companion:
            companion = {}

        if user_id:
            companion[Like.USER_ID] = user_id

        if post_id:
            companion[Like.POST_ID] = post_id

        self.companion = companion

    def get_user_id(self):
        return self.get_obj()[Like.USER_ID]

    def get_post_id(self):
        return self.get_obj()[Like.POST_ID]

    def get_obj(self):
        if not self.companion.get(Like.CREATED_TIME):
            self.companion[Like.CREATED_TIME] = ttm_util.now()

        return self.companion
