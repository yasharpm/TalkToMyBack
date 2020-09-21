from entity.base_entity import BaseEntity
from entity.repositories import *


class Post(BaseEntity):

    USER_ID = 'user_id'
    USER_NAME = 'user_name'
    USER_ANONYMOUS = 'user_anonymous'
    CONTENT = 'content'
    LANGUAGE = 'language'
    COUNTRY = 'country'
    COMMUNITY = 'community'
    COMMENT_COUNT = 'comment_count'
    LIKE_COUNT = 'like_count'
    VIEW_COUNT = 'view_count'
    REPORT_COUNT = 'report_count'
    COMMENTS = 'comments'
    LIKES = 'likes'
    REPORTS = 'reports'

    UTIL_POST_COUNT = 'util_post_count'

    def __init__(self, user_id=None, user_name=None, user_anonymous=None, content=None, language=None, country=None,
                 community=None, companion=None):
        if not companion:
            companion = {}

        if user_id:
            companion[Post.USER_ID] = user_id

        if user_name:
            companion[Post.USER_NAME] = user_name

        if user_anonymous is not None:
            companion[Post.USER_ANONYMOUS] = user_anonymous

        if content:
            companion[Post.CONTENT] = content

        if language:
            companion[Post.LANGUAGE] = language

        if country:
            companion[Post.COUNTRY] = country

        if community:
            companion[Post.COMMUNITY] = community

        BaseEntity.__init__(self, companion)

    def get_obj(self):
        obj = super(Post, self).get_obj()

        if not obj.get(Post.USER_ANONYMOUS):
            obj[Post.USER_ANONYMOUS] = False

        if not obj.get(Post.COMMUNITY):
            obj[Post.COMMUNITY] = COMMUNITY_REPO.get_public_community_number()

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

        if public_obj[Post.USER_ANONYMOUS]:
            public_obj[Post.USER_ID] = None
            public_obj[Post.USER_NAME] = None

        community_number = public_obj.get(Post.COMMUNITY)
        community = COMMUNITY_REPO.get_community_by_number(community_number)

        if not community:
            community_id = None
        else:
            community_id = community.get_public_id()

        public_obj[Post.COMMUNITY] = community_id

        return public_obj

    def get_user_id(self):
        return self.get_obj().get(Post.USER_ID)

    def get_view_count(self):
        return self.get_obj().get(Post.VIEW_COUNT)
