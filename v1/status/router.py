import v1.status.client.router


def setup(app, prefix):
    prefix = prefix + '/status'

    v1.status.client.router.setup(app, prefix)
