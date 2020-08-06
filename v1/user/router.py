import v1.user.register
import v1.user.refreshToken
import v1.user.updateFCMToken
import v1.user._


def setup(app, prefix):
    prefix = prefix + '/user'

    v1.user.register.setup(app, prefix)
    v1.user.refreshToken.setup(app, prefix)
    v1.user.updateFCMToken.setup(app, prefix)
    v1.user._.setup(app, prefix)
