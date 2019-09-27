import falcon
from itertools import groupby

from v1.authentication import authenticate
from entity.post.post_repo import PostRepo
from entity.user.user_repo import UserRepo
from entity.sync.sync_repo import SyncRepo


class seen:

    def on_post(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        post_ids = req.media.get('postIds')

        if not post_ids:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Require post ids.'}
            return

        if not isinstance(post_ids, list):
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'postIds must be an array of post ids.'}
            return

        user_repo = UserRepo()

        user_repo.on_viewed_posts(user, len(post_ids))

        # We can cache the list of ids to process them later in batch. Not by every request.
        # The logic in app also tries to send the view notices in batch.

        # The algorithm here aggregates twice:
        # First time on post ids, to avoid retrieving the same post multiple times.
        # Second time on user ids, to avoid retrieving the same user multiple times.

        post_ids = sorted(post_ids)

        post_repo = PostRepo()
        sync_repo = SyncRepo()

        aggregated_affected_users = {}

        processed_post_ids = []

        for post_id, values in groupby(post_ids):
            view_count = len(list(values))

            post = post_repo.on_post_viewed(post_id, view_count)

            if not post:
                continue

            processed_post_ids.append(post_id)

            affected_user = post.get_user_id()

            affected_posts = aggregated_affected_users.get(affected_user, {})

            affected_posts[post.get_mongo_id()] = post.get_view_count()

            aggregated_affected_users[affected_user] = affected_posts

            sync_repo.new_view(actor=user.get_public_id(), affected=post.get_user_id(), post_id=post.get_public_id(),
                               views=view_count)

        for user_id in aggregated_affected_users:
            affected_posts = aggregated_affected_users[user_id]

            user_repo.set_view_on_posts(user_id, affected_posts)

        resp.status = falcon.HTTP_200
        resp.media = {'postIds': processed_post_ids}


def setup(app, prefix):
    app.add_route(prefix + '/seen', seen())
