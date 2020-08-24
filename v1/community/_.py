import falcon

from entity.repositories import COMMUNITY_REPO
from entity.community.community_errors import *


class _:

    def on_post(self, req, resp):
        token = req.get_header('token')

        if token != 'iamnotanasshole':
            resp.status = falcon.HTTP_401  # Unauthorized
            resp.media = {'message': 'You do not have permission to perform this action. Please be polite.'}
            return

        parent_id = req.media.get('parent_id')
        name = req.media.get('name')

        if not parent_id:
            parent_id = None
        else:
            parent_id = bytes.fromhex(parent_id)

        community = COMMUNITY_REPO.new_community(parent_id=parent_id, name=name)

        if community == COMMUNITY_DOES_NOT_EXIST:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Parent community id not found.'}
            return

        if community == OVERFLOWING_CHILD_COUNT:
            resp.status = falcon.HTTP_406  # Not acceptable
            resp.media = {'message': 'This community can not have any more children.'}
            return

        resp.status = falcon.HTTP_200
        resp.media = community.get_public_obj()

    def on_get(self, req, resp):
        id = req.get_param('id')
        return_tree = req.get_param_as_bool('tree', default=False)

        if not id:
            id = None
        else:
            id = bytes.fromhex(id)

        if return_tree:
            tree = COMMUNITY_REPO.get_community_tree(id)

            if tree is None:
                resp.status = falcon.HTTP_404  # Not found
                resp.media = {'message': 'Community id not found.'}
                return

            resp.status = falcon.HTTP_200
            resp.media = tree
            return

        community = COMMUNITY_REPO.get_community(id)

        if not community:
            resp.status = falcon.HTTP_404  # Not found
            resp.media = {'message': 'Community id not found.'}
            return

        resp.status = falcon.HTTP_200
        resp.media = community.get_public_obj()


def setup(app, prefix):
    app.add_route(prefix, _())
