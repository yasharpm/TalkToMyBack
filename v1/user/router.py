import v1.user.register
import v1.user.refreshToken


def setup(app, prefix):
    prefix = prefix + '/user'

    v1.user.register.setup(app, prefix)
    v1.user.refreshToken.setup(app, prefix)
