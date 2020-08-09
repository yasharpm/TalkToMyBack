import falcon

import ttm_util
from entity.repositories import POST_REPO

MAXIMUM_RANDOM_POST_COUNT = 50


class exhibition:

    def on_get(self, req, resp):
        count = req.get_param_as_int('count', min_value=1, max_value=MAXIMUM_RANDOM_POST_COUNT)
        day = req.get_param_as_int('day', min_value=0)
        week = req.get_param_as_int('week', min_value=0)
        month = req.get_param_as_int('month', min_value=0)
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

        posts = POST_REPO.exhibition_posts(count, language, country, day, week, month)
        
        resp.status = falcon.HTTP_200
        resp.media = {'posts': posts}


def setup(app, prefix):
    app.add_route(prefix + '/exhibition', exhibition())
