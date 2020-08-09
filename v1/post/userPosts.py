import falcon

from v1.authentication import authenticate
from entity.user.user import User
from entity.repositories import USER_REPO
from entity.post.post import Post

MAXIMUM_COUNT = 50


class userPosts:

    def on_get(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        user_id = req.get_param('id')
        count = req.get_param_as_int('count', min_value=1, max_value=MAXIMUM_COUNT, default=10)
        offset = req.get_param_as_int('offset', min_value=0, default=0)

        raw_user_id = bytes.fromhex(user_id)
        user = USER_REPO.find_user(raw_user_id)

        if not user:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.media = {'message': 'User id not found.'}
            return

        user_obj = user.get_public_obj()

        total_count = user_obj[User.POSTED_POSTS_COUNT]

        all_posts = user_obj[User.POSTS]
        posts_with_offset = all_posts[offset:offset + count]

        count = len(posts_with_offset)

        posts = []

        for post_obj in posts_with_offset:
            posts.append(Post(companion=post_obj).get_public_obj())

        resp.status = falcon.HTTP_200
        resp.media = {'totalCount': total_count, 'count': count, 'data': posts}


def setup(app, prefix):
    app.add_route(prefix + '/userPosts', userPosts())
