import falcon

from v1.authentication import authenticate
from entity.post.post_util import validate
from entity.repositories import COMMUNITY_REPO
from entity.repositories import USER_REPO
from entity.repositories import POST_REPO
from entity.repositories import SYNC_REPO
from entity.community.community import Community


class _:

    def on_post(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        post_content = req.media.get('post')
        language = req.media.get('language')
        country = req.media.get('country')
        community = req.media.get('community')

        if not validate(post_content, language, country, resp):
            return

        if not community:
            community = COMMUNITY_REPO.get_public_community_number()
        else:
            community = COMMUNITY_REPO.get_community_by_id_name(community)

            if not community:
                resp.status = falcon.HTTP_400  # Bad request
                resp.media = {'message': 'Community id name not found.'}
                return

            community = community.get_obj()[Community.NUMBER]

        post = POST_REPO.new_post(user, post_content, language, country, community)

        USER_REPO.on_new_post(user, post)

        sync = SYNC_REPO.new_post(post)

        resp.status = falcon.HTTP_200
        resp.media = post.get_public_obj()

    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Max-Age', 86400)  # One day

        token = req.get_header('token')

        if token != 'web':
            user = authenticate(req, resp)

            if not user:
                return

        post_id = req.get_param('id')

        post = POST_REPO.find_post(post_id)

        if not post:
            resp.status = falcon.HTTP_404  # Not found
            resp.media = {'message': 'Post not found.'}
            return

        resp.status = falcon.HTTP_200
        resp.media = post.get_public_obj()


    def on_options(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Max-Age', 86400)  # One day
        resp.media = {'message': 'OK'}


def setup(app, prefix):
    app.add_route(prefix, _())
