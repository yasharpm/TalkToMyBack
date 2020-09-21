import falcon

import ttm_util
from entity.repositories import COMMUNITY_REPO
from entity.repositories import POST_REPO
from entity.community.community_errors import *

MAXIMUM_RANDOM_POST_COUNT = 50


class exhibition:

    def on_get(self, req, resp):
        count = req.get_param_as_int('count', min_value=1, max_value=MAXIMUM_RANDOM_POST_COUNT)
        day = req.get_param_as_int('day', min_value=0)
        week = req.get_param_as_int('week', min_value=0)
        month = req.get_param_as_int('month', min_value=0)
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
            community = bytes.fromhex(community)

        posts = POST_REPO.exhibition_posts(count, language, country, community, day, week, month)

        if posts == COMMUNITY_DOES_NOT_EXIST:
            resp.status = falcon.HTTP_404  # Not found
            resp.media = {'message': 'Community not found'}
            return
        
        resp.status = falcon.HTTP_200
        resp.media = {'posts': posts}


def setup(app, prefix):
    app.add_route(prefix + '/exhibition', exhibition())
