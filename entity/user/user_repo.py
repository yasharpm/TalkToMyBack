import pymongo
from passlib.hash import pbkdf2_sha256

from entity.base_repo import BaseRepo
from entity.user.user import User
from entity.post.post import Post
from entity.like.like import Like


class UserRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, 'user')

        self.db.create_index([(User.POSTED_POSTS_COUNT, pymongo.HASHED)], name='user_id')
        self.db.create_index([(User.POSTED_COMMENTS_COUNT, pymongo.HASHED)], name='comments_count')
        self.db.create_index([(User.POSTED_LIKES_COUNT, pymongo.HASHED)], name='likes_count')
        self.db.create_index([(User.REPORTED_POSTS_COUNT, pymongo.HASHED)], name='reported_posts_count')
        self.db.create_index([(User.POSTED_VIEWS_COUNT, pymongo.HASHED)], name='posted_views_count')
        self.db.create_index([(User.REPORTS_ON_USER_COUNT, pymongo.HASHED)], name='reports_on_user_count')

    def new_user(self, raw_password):
        hashed_password = pbkdf2_sha256.hash(raw_password)

        user = User(password_hash=hashed_password)

        result = self.db.insert_one(user.get_obj())

        user.set_mongo_id(result.inserted_id)

        return user

    def find_user(self, user_id):
        companion = self.db.find_one({User.MONGO_ID: user_id})

        if companion:
            return User(companion=companion)

        return None

    def on_new_post(self, user, post):
        user_obj = user.get_obj()

        user_obj[User.POSTS].insert(0, post.get_obj())
        user_obj[User.POSTED_POSTS_COUNT] += 1

        user.on_updated()

        self.db.update_one(
            {User.MONGO_ID: user_obj[User.MONGO_ID]},
            {"$set": {
                User.POSTS: user_obj[User.POSTS],
                User.POSTED_POSTS_COUNT: user_obj[User.POSTED_POSTS_COUNT],
                User.UPDATED_TIME: user_obj[User.UPDATED_TIME]
            }}
        )

    def on_viewed_posts(self, user, count):
        user_obj = user.get_obj()

        user_obj[User.POSTED_VIEWS_COUNT] += count

        user.on_updated()

        self.db.update_one(
            {User.MONGO_ID: user_obj[User.MONGO_ID]},
            {"$set": {
                User.POSTED_VIEWS_COUNT: user_obj[User.POSTED_VIEWS_COUNT],
                User.UPDATED_TIME: user_obj[User.UPDATED_TIME]
            }}
        )

    def set_view_on_posts(self, user_id, posts):
        real_user_id = bytes.fromhex(user_id)

        user_obj = self.db.find_one({User.ID: real_user_id})

        all_posts = user_obj[User.POSTS]

        for post in all_posts:
            post_id = post[Post.MONGO_ID]

            if post_id in posts:
                post[Post.VIEW_COUNT] = posts[post_id]

        self.db.update_one(
            {User.MONGO_ID: user_obj[User.MONGO_ID]},
            {"$set": {
                User.POSTS: all_posts
            }}
        )

    def update_user_post(self, post):
        user_id = bytes.fromhex(post.get_user_id())

        user_obj = self.db.find_one({User.ID: user_id})

        user = User(companion=user_obj)

        user.on_updated()

        user_obj = user.get_obj()

        posts = user_obj[User.POSTS]

        post_id = post.get_obj()[Post.ID]

        index = next((index for (index, post_obj) in enumerate(posts) if post_obj[Post.ID] == post_id), -1)

        if index >= 0:
            posts[index] = post.get_obj()

            self.db.update_one(
                {User.MONGO_ID: user_obj[User.MONGO_ID]},
                {"$set": {
                    User.POSTS: posts,
                    User.UPDATED_TIME: user_obj[User.UPDATED_TIME]
                }}
            )

    def on_new_comment(self, user, comment):
        user_obj = user.get_obj()

        user_obj[User.COMMENTS].insert(0, comment.get_obj())
        user_obj[User.POSTED_COMMENTS_COUNT] += 1

        user.on_updated()

        self.db.update_one(
            {User.MONGO_ID: user_obj[User.MONGO_ID]},
            {"$set": {
                User.COMMENTS: user_obj[User.COMMENTS],
                User.POSTED_COMMENTS_COUNT: user_obj[User.POSTED_COMMENTS_COUNT],
                User.UPDATED_TIME: user_obj[User.UPDATED_TIME]
            }}
        )

    def on_new_like(self, user, like, liked):
        user_obj = user.get_obj()

        likes = user_obj[User.LIKES]

        user_id = like.get_user_id()
        post_id = like.get_post_id()

        index = next((index for (index, like_obj) in enumerate(likes) if like_obj[Like.USER_ID] == user_id and
                      like_obj[Like.POST_ID] == post_id), -1)

        if index >= 0:
            if liked:
                #  Already liked
                return
            else:
                likes.pop(index)
                user_obj[User.POSTED_LIKES_COUNT] -= 1
        else:
            if liked:
                likes.insert(0, like.get_obj())
                user_obj[User.POSTED_LIKES_COUNT] += 1
            else:
                #  Already not liked
                return

        user.on_updated()

        self.db.update_one(
            {User.MONGO_ID: user_obj[User.MONGO_ID]},
            {"$set": {
                User.LIKES: user_obj[User.LIKES],
                User.POSTED_LIKES_COUNT: user_obj[User.POSTED_LIKES_COUNT],
                User.UPDATED_TIME: user_obj[User.UPDATED_TIME]
            }}
        )

    def on_new_report(self, user, report):
        user_obj = user.get_obj()

        user_obj[User.REPORTS].insert(0, report.get_obj())
        user_obj[User.REPORTED_POSTS_COUNT] += 1

        user.on_updated()

        self.db.update_one(
            {User.MONGO_ID: user_obj[User.MONGO_ID]},
            {"$set": {
                User.REPORTS: user_obj[User.REPORTS],
                User.REPORTED_POSTS_COUNT: user_obj[User.REPORTED_POSTS_COUNT],
                User.UPDATED_TIME: user_obj[User.UPDATED_TIME]
            }}
        )

    def on_report_on_user(self, user_id, report):
        user_id = bytes.fromhex(user_id)

        user_obj = self.db.find_one({User.ID: user_id})

        user = User(companion=user_obj)

        user_obj = user.get_obj()

        user_obj[User.REPORTS_ON_USER].insert(0, report.get_obj())
        user_obj[User.REPORTS_ON_USER_COUNT] += 1

        user.on_updated()

        self.db.update_one(
            {User.MONGO_ID: user_obj[User.MONGO_ID]},
            {"$set": {
                User.REPORTS_ON_USER: user_obj[User.REPORTS_ON_USER],
                User.REPORTS_ON_USER_COUNT: user_obj[User.REPORTS_ON_USER_COUNT],
                User.UPDATED_TIME: user_obj[User.UPDATED_TIME]
            }}
        )
