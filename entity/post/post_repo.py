import pymongo

from entity.base_repo import BaseRepo
from entity.post.post import Post
from entity.like.like import Like


class PostRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, 'post')

        self.db.create_index([(Post.USER_ID, pymongo.HASHED)], name='user_id')
        self.db.create_index([(Post.VIEW_COUNT, pymongo.HASHED)], name='view_count')
        self.db.create_index([(Post.REPORT_COUNT, pymongo.HASHED)], name='report_count')

    def new_post(self, user, content, language, country):
        post = Post(user_id=user.get_public_id(), content=content, language=language, country=country)

        result = self.db.insert_one(post.get_obj())

        post.set_mongo_id(result.inserted_id)

        return post

    def random_posts(self, count, language, country, processed=True):
        match = {}

        if language:
            match[Post.LANGUAGE] = language

        if country:
            match[Post.COUNTRY] = country

        if len(match) > 0:
            post_objs = self.db.aggregate([{'$match': match}, {'$sample': {'size': count}}])
        else:
            post_objs = self.db.aggregate([{'$sample': {'size': count}}])

        posts = []

        if processed:
            for post_obj in post_objs:
                posts.append(Post(companion=post_obj).get_public_obj())
        else:
            for post_obj in post_objs:
                posts.append(Post(companion=post_obj))

        return posts

    def on_post_viewed(self, post_id, view_count):
        post = self.find_post(post_id)

        if not post:
            return None

        post.on_updated()

        post_obj = post.get_obj()

        post_obj[Post.VIEW_COUNT] += view_count

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.VIEW_COUNT: post_obj[Post.VIEW_COUNT],
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post

    def on_new_comment(self, comment):
        post = self.find_post(comment.get_post_id())

        if not post:
            return None

        post.on_updated()

        post_obj = post.get_obj()

        post_obj[Post.COMMENTS].insert(0, comment.get_obj())
        post_obj[Post.COMMENT_COUNT] += 1

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.COMMENT_COUNT: post_obj[Post.COMMENT_COUNT],
                Post.COMMENTS: post_obj[Post.COMMENTS],
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post

    def on_new_like(self, like, liked):
        post = self.find_post(like.get_post_id())

        if not post:
            return None, False

        post.on_updated()

        post_obj = post.get_obj()

        likes = post_obj[Post.LIKES]

        user_id = like.get_user_id()

        index = next((index for (index, like_obj) in enumerate(likes) if like_obj[Like.USER_ID] == user_id), -1)

        if index >= 0:
            if liked:
                #  Already liked
                return post, False
            else:
                likes.pop(index)
        else:
            if liked:
                likes.insert(0, like.get_obj())
            else:
                #  Already not liked
                return post, False

        post_obj[Post.LIKE_COUNT] = len(likes)

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.LIKE_COUNT: post_obj[Post.LIKE_COUNT],
                Post.LIKES: likes,
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post, True

    def find_post(self, post_id):
        post_id = bytes.fromhex(post_id)

        post_obj = self.db.find_one({Post.ID: post_id})

        if not post_obj:
            return None

        post = Post(companion=post_obj)

        return post

    def on_new_report(self, post, report):
        post.on_updated()

        post_obj = post.get_obj()

        post_obj[Post.REPORTS].insert(0, report.get_obj())
        post_obj[Post.REPORT_COUNT] += 1

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.REPORT_COUNT: post_obj[Post.REPORT_COUNT],
                Post.REPORTS: post_obj[Post.REPORTS],
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post
