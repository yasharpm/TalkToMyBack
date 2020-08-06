from entity.base_entity import BaseEntity


class User(BaseEntity):

    PASSWORD = 'password'
    NAME = 'name'
    ABOUT = 'about'
    CONTACT = 'contact'
    POSTED_POSTS_COUNT = 'postedPostsCount'
    POSTED_COMMENTS_COUNT = 'postedCommentsCount'
    POSTED_LIKES_COUNT = 'postedLikesCount'
    REPORTED_POSTS_COUNT = 'reportedPostsCount'
    POSTED_VIEWS_COUNT = 'postedViewsCount'
    REPORTS_ON_USER_COUNT = 'reportsOnUserCount'
    POSTS = 'posts'
    COMMENTS = 'comments'
    LIKES = 'likes'
    REPORTS = 'reports'
    REPORTS_ON_USER = 'reportsOnUser'
    FCM_TOKEN = 'fcmToken'

    def __init__(self, password_hash=None, companion=None):
        if not companion:
            companion = {}

        if password_hash:
            companion[User.PASSWORD] = password_hash

        BaseEntity.__init__(self, companion)

    def get_obj(self):
        obj = super(User, self).get_obj()

        if not obj.get(User.NAME):
            obj[User.NAME] = None

        if not obj.get(User.ABOUT):
            obj[User.ABOUT] = None

        if not obj.get(User.CONTACT):
            obj[User.CONTACT] = None

        if not obj.get(User.POSTED_VIEWS_COUNT):
            obj[User.POSTED_VIEWS_COUNT] = 0

        if not obj.get(User.POSTS):
            obj[User.POSTS] = []

        if not obj.get(User.COMMENTS):
            obj[User.COMMENTS] = []

        if not obj.get(User.LIKES):
            obj[User.LIKES] = []

        if not obj.get(User.REPORTS):
            obj[User.REPORTS] = []

        if not obj.get(User.REPORTS_ON_USER):
            obj[User.REPORTS_ON_USER] = []

        obj[User.POSTED_POSTS_COUNT] = len(obj[User.POSTS])
        obj[User.POSTED_COMMENTS_COUNT] = len(obj[User.COMMENTS])
        obj[User.POSTED_LIKES_COUNT] = len(obj[User.LIKES])
        obj[User.REPORTED_POSTS_COUNT] = len(obj[User.REPORTS])
        obj[User.REPORTS_ON_USER_COUNT] = len(obj[User.REPORTS_ON_USER])

        return obj

    def get_public_obj(self):
        obj = BaseEntity.get_public_obj(self)

        obj.pop(User.PASSWORD, None)
        obj.pop(User.REPORTS_ON_USER_COUNT, None)
        obj.pop(User.POSTS, None)
        obj.pop(User.COMMENTS, None)
        obj.pop(User.LIKES, None)
        obj.pop(User.REPORTS, None)
        obj.pop(User.REPORTS_ON_USER, None)
        obj.pop(User.FCM_TOKEN, None)
