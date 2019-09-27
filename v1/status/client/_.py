import falcon

LATEST_VERSION_CODE = 1
LATEST_VERSION_NAME = '1.0.0'

UPDATE_FORCED = 'forced'
UPDATE_SUGGESTED = 'suggested'
UPDATE_NONE = 'none'


class _:

    def on_get(self, req, resp):
        client = req.get_param('client', default=None)
        version_code = req.get_param('versionCode', default=None)

        # We do stuff here.

        resp.status = falcon.HTTP_200
        resp.media = {
            'latestVersionCode': LATEST_VERSION_CODE,
            'latestVersionName': LATEST_VERSION_NAME,
            'updateRequired': UPDATE_SUGGESTED
        }


def setup(app, prefix):
    app.add_route(prefix, _())
