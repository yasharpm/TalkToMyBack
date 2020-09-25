import falcon

from entity.repositories import COMMUNITY_REPO
from entity.community.community_errors import *
from entity.community.community import Community


class _:

    def on_post(self, req, resp):
        token = req.get_header('token')

        if token != 'iamnotanasshole':
            resp.status = falcon.HTTP_401  # Unauthorized
            resp.media = {'message': 'You do not have permission to perform this action. Please be nice.'}
            return

        parent_id = req.media.get('parent_id')
        name = req.media.get('name')
        description = req.media.get('description')
        id_name = req.media.get('id_name')

        if not parent_id:
            parent_id = None
        else:
            parent_id = bytes.fromhex(parent_id)

        community = COMMUNITY_REPO.new_community(parent_id=parent_id, name=name, description=description,
                                                 id_name=id_name)

        if community == COMMUNITY_DOES_NOT_EXIST:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Parent community id not found.'}
            return

        if community == OVERFLOWING_CHILD_COUNT:
            resp.status = falcon.HTTP_406  # Not acceptable
            resp.media = {'message': 'This community can not have any more children.'}
            return

        if community == ID_NAME_DUPLICATE:
            resp.status = falcon.HTTP_406  # Not acceptable
            resp.media = {'message': 'Id name already exists.'}
            return

        resp.status = falcon.HTTP_200
        resp.media = community.get_public_obj()

    def on_get(self, req, resp):
        id = req.get_param('id', default=None)
        id_name = req.get_param('id_name', default=None)
        return_tree = req.get_param_as_bool('tree', default=False)

        if id is not None:
            if len(id) > 0:
                id = bytes.fromhex(id)
            else:
                id = None

        if id_name is not None and len(id_name) > 0:
            community = COMMUNITY_REPO.get_community_by_id_name(id_name)
            id = community.get_obj()[Community.ID]

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
