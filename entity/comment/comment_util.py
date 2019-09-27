import falcon

MINIMUM_CONTENT_LENGTH = 1


def validate(content, resp):
    if not content or len(content) < MINIMUM_CONTENT_LENGTH:
        resp.status = falcon.HTTP_406  # Not acceptable
        resp.media = {'message': 'Comment content is too short.'}
        return False

    return True
