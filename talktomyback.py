from wsgiref.simple_server import make_server
import falcon

import notification.gonification

import v1.router

app = falcon.API()

v1.router.setup(app, '/api')

if __name__ == '__main__':
    notification.gonification.init()

    httpd = make_server('', 8000, app)
    print('Serving on port 8000...')

    httpd.serve_forever()
