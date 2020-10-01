import falcon

import ttm_util
from v1.authentication import authenticate
from entity.repositories import COMMUNITY_REPO
from entity.repositories import POST_REPO
from entity.community.community_errors import *
from entity.community.community import Community

MAXIMUM_RANDOM_POST_COUNT = 50


class random:

    def on_get(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        count = req.get_param_as_int('count', min_value=1, max_value=MAXIMUM_RANDOM_POST_COUNT)
        language = req.get_param('language')
        country = req.get_param('country')
        community = req.get_param('community')

        if language and not ttm_util.validate_language(language):
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Invalid language code'}
            return

        if country and not ttm_util.validate_country(country):
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Invalid country code'}
            return

        if community is None or len(community) == 0:
            community = COMMUNITY_REPO.get_public_community_id()
        else:
            community = COMMUNITY_REPO.get_community_by_id_name(community)

            if community is not None:
                community = community.get_obj()[Community.ID]
            else:
                resp.status = falcon.HTTP_404  # Not found
                resp.media = {'message': 'Community not found'}
                return

        posts = POST_REPO.random_posts(count, language, country, community)

        if posts == COMMUNITY_DOES_NOT_EXIST:
            resp.status = falcon.HTTP_404  # Not found
            resp.media = {'message': 'Community not found'}
            return
        
        resp.status = falcon.HTTP_200
        resp.media = {'posts': posts}


def setup(app, prefix):
    app.add_route(prefix + '/random', random())
