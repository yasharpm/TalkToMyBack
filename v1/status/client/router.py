import v1.status.client._


def setup(app, prefix):
    prefix = prefix + '/client'

    v1.status.client._.setup(app, prefix)
