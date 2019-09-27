import falcon

from v1.authentication import authenticate
from entity.like.like import Like
from entity.post.post_repo import PostRepo
from entity.user.user_repo import UserRepo
from entity.sync.sync_repo import SyncRepo


class _:

    def on_post(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        post_id = req.media.get('postId')
        liked = req.media.get('like')

        if not post_id:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Post id is not given.'}
            return

        if liked is None:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': '"like" boolean is not set.'}
            return

        if not isinstance(liked, bool):
            if liked.lower() == 'true':
                liked = True
            else:
                if liked.lower == 'false':
                    liked = False
                else:
                    resp.status = falcon.HTTP_400  # Bad request
                    resp.media = {'message': '"like" must either be true or false.'}
                    return

        like = Like(user_id=user.get_public_id(), post_id=post_id)

        (post, has_change) = PostRepo().on_new_like(like, liked)

        if not post:
            resp.status = falcon.HTTP_406  # Not acceptable
            resp.media = {'message': 'Post id does not exist.'}
            return

        if not has_change:
            resp.status = falcon.HTTP_200
            resp.media = like.get_obj()
            return

        user_repo = UserRepo()

        user_repo.update_user_post(post)

        user_repo.on_new_like(user, like, liked)

        sync = SyncRepo().new_like(actor=user.get_public_id(), affected=post.get_user_id(), like=like, liked=liked)

        if liked:
            #  TODO Use sync to send a notification.
            pass

        resp.status = falcon.HTTP_200
        resp.media = like.get_obj()


def setup(app, prefix):
    app.add_route(prefix, _())
