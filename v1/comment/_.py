import falcon

from v1.authentication import authenticate
from entity.comment.comment_util import validate
from entity.comment.comment import Comment
from entity.post.post_repo import PostRepo
from entity.user.user_repo import UserRepo
from entity.sync.sync_repo import SyncRepo
from notification import gotification

MINIMUM_COMMENT_LENGTH = 1


class _:

    def on_post(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        post_id = req.media.get('postId')
        content = req.media.get('comment')

        if not post_id:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Post id is not given.'}
            return

        if not validate(content, resp):
            return

        comment = Comment(user_id=user.get_public_id(), post_id=post_id, content=content)

        post = PostRepo().on_new_comment(comment)

        if not post:
            resp.status = falcon.HTTP_406  # Not acceptable
            resp.media = {'message': 'Post id does not exist.'}
            return

        user_repo = UserRepo()

        receiving_user = user_repo.update_user_post(post)

        user_repo.on_new_comment(user, comment)

        sync = SyncRepo().new_comment(actor=user.get_public_id(), affected=post.get_user_id(), comment=comment)

        # Use sync to send a notification.
        gotification.send_notification(receiving_user, sync)

        resp.status = falcon.HTTP_200
        resp.media = comment.get_obj()


def setup(app, prefix):
    app.add_route(prefix, _())
