from entity.base_entity import BaseEntity


class Post(BaseEntity):

    USER_ID = 'user_id'
    CONTENT = 'content'
    LANGUAGE = 'language'
    COUNTRY = 'country'
    COMMENT_COUNT = 'comment_count'
    LIKE_COUNT = 'like_count'
    VIEW_COUNT = 'view_count'
    REPORT_COUNT = 'report_count'
    COMMENTS = 'comments'
    LIKES = 'likes'
    REPORTS = 'reports'

    UTIL_POST_COUNT = 'util_post_count'

    def __init__(self, user_id=None, content=None, language=None, country=None, companion=None):
        if not companion:
            companion = {}

        if user_id:
            companion[Post.USER_ID] = user_id

        if content:
            companion[Post.CONTENT] = content

        if language:
            companion[Post.LANGUAGE] = language

        if country:
            companion[Post.COUNTRY] = country

        BaseEntity.__init__(self, companion)

    def get_obj(self):
        obj = super(Post, self).get_obj()

        if not obj.get(Post.COMMENT_COUNT):
            obj[Post.COMMENT_COUNT] = 0

        if not obj.get(Post.LIKE_COUNT):
            obj[Post.LIKE_COUNT] = 0

        if not obj.get(Post.VIEW_COUNT):
            obj[Post.VIEW_COUNT] = 1

        if not obj.get(Post.REPORT_COUNT):
            obj[Post.REPORT_COUNT] = 0

        if not obj.get(Post.COMMENTS):
            obj[Post.COMMENTS] = []

        if not obj.get(Post.LIKES):
            obj[Post.LIKES] = []

        if not obj.get(Post.REPORTS):
            obj[Post.REPORTS] = []

        if not obj.get(Post.UTIL_POST_COUNT):
            obj[Post.UTIL_POST_COUNT] = None

        return obj

    def get_public_obj(self):
        public_obj = BaseEntity.get_public_obj(self)

        public_obj.pop(Post.REPORTS, None)
        public_obj.pop(Post.UTIL_POST_COUNT, None)

        return public_obj

    def get_user_id(self):
        return self.get_obj().get(Post.USER_ID)

    def get_view_count(self):
        return self.get_obj().get(Post.VIEW_COUNT)
