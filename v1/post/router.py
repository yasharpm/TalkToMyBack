import v1.post._
import v1.post._random
import v1.post.myPosts
import v1.post.seen


def setup(app, prefix):
    prefix = prefix + '/post'

    v1.post._.setup(app, prefix)
    v1.post._random.setup(app, prefix)
    v1.post.myPosts.setup(app, prefix)
    v1.post.seen.setup(app, prefix)
