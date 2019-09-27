import v1.like._


def setup(app, prefix):
    prefix = prefix + '/like'

    v1.like._.setup(app, prefix)
