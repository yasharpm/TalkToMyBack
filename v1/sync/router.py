import v1.sync._


def setup(app, prefix):
    prefix = prefix + '/sync'

    v1.sync._.setup(app, prefix)
