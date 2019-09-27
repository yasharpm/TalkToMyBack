import v1.user.router
import v1.post.router
import v1.comment.router
import v1.like.router
import v1.report.router
import v1.sync.router


def setup(app, prefix):
    prefix = prefix + '/v1'

    v1.user.router.setup(app, prefix)
    v1.post.router.setup(app, prefix)
    v1.comment.router.setup(app, prefix)
    v1.like.router.setup(app, prefix)
    v1.report.router.setup(app, prefix)
    v1.sync.router.setup(app, prefix)
