import v1.community._


def setup(app, prefix):
    prefix = prefix + '/community'

    v1.community._.setup(app, prefix)
