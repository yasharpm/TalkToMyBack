import uuid
import ttm_util


class Comment:

    ID = 'id'
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'

    USER_ID = 'user_id'
    POST_ID = 'post_id'
    CONTENT = 'content'

    def __init__(self, user_id=None, post_id=None, content=None, companion=None):
        if not companion:
            companion = {}

        if user_id:
            companion[Comment.USER_ID] = user_id

        if post_id:
            companion[Comment.POST_ID] = post_id

        if content:
            companion[Comment.CONTENT] = content

        self.companion = companion

    def get_user_id(self):
        return self.get_obj()[Comment.USER_ID]

    def get_post_id(self):
        return self.get_obj()[Comment.POST_ID]

    def on_updated(self):
        self.get_obj()[Comment.UPDATED_TIME] = ttm_util.now()

    def get_obj(self):
        if not self.companion.get(Comment.CREATED_TIME):
            self.companion[Comment.CREATED_TIME] = ttm_util.now()

        if not self.companion.get(Comment.UPDATED_TIME):
            self.companion[Comment.UPDATED_TIME] = self.companion[Comment.CREATED_TIME]

        if not self.companion.get(Comment.ID):
            self.companion[Comment.ID] = uuid.uuid4().bytes.hex()

        return self.companion
