import falcon

import ttm_util
from v1.authentication import authenticate
from entity.post.post_repo import PostRepo

MAXIMUM_RANDOM_POST_COUNT = 50


class random:

    def on_get(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        count = req.get_param_as_int('count', min_value=1, max_value=MAXIMUM_RANDOM_POST_COUNT)
        language = req.get_param('language')
        country = req.get_param('country')

        if language and not ttm_util.validate_language(language):
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Invalid language code'}
            return

        if country and not ttm_util.validate_country(country):
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Invalid country code'}
            return

        posts = PostRepo().random_posts(count, language, country)
        
        resp.status = falcon.HTTP_200
        resp.media = {'posts': posts}


def setup(app, prefix):
    app.add_route(prefix + '/random', random())
