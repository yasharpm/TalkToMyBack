import v1.comment._


def setup(app, prefix):
    prefix = prefix + '/comment'

    v1.comment._.setup(app, prefix)
