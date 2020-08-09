import falcon

from v1.authentication import authenticate
from entity.repositories import SYNC_REPO

MAX_SYNC_OBJECT_COUNT = 20


class _:

    def on_get(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        update_token = req.get_param('updateToken', default=None)

        (syncs, new_update_token, has_more) = SYNC_REPO.sync(user, update_token, MAX_SYNC_OBJECT_COUNT)

        resp.status = falcon.HTTP_200
        resp.media = {'updateToken': new_update_token, 'syncCompleted': not has_more, 'changes': syncs}


def setup(app, prefix):
    app.add_route(prefix, _())
