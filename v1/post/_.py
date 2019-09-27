import falcon

from v1.authentication import authenticate
from entity.post.post_util import validate
from entity.post.post_repo import PostRepo
from entity.user.user_repo import UserRepo
from entity.sync.sync_repo import SyncRepo


class _:

    def on_post(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        post_content = req.media.get('post')
        language = req.media.get('language')
        country = req.media.get('country')

        if not validate(post_content, language, country, resp):
            return

        post = PostRepo().new_post(user, post_content, language, country)

        UserRepo().on_new_post(user, post)

        sync = SyncRepo().new_post(post)

        resp.status = falcon.HTTP_200
        resp.media = post.get_public_obj()


def setup(app, prefix):
    app.add_route(prefix, _())
