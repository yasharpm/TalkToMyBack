import falcon

import ttm_util

MINIMUM_CONTENT_LENGTH = 24


def validate(content, language, country, resp):
    if not ttm_util.validate_language(language):
        resp.status = falcon.HTTP_400  # Bad request
        resp.media = {'message': 'Invalid or no language code provided.'}
        return False

    if not ttm_util.validate_country(country):
        resp.status = falcon.HTTP_400  # Bad request
        resp.media = {'message': 'Invalid or no country code provided.'}
        return False

    if not content or len(content) < MINIMUM_CONTENT_LENGTH:
        resp.status = falcon.HTTP_406  # Not acceptable
        resp.media = {'message': 'Post content is too short.'}
        return False

    return True
