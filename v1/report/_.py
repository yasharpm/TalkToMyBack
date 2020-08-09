import falcon

from v1.authentication import authenticate
from entity.report.report import Report
from entity.repositories import USER_REPO
from entity.repositories import POST_REPO


class _:

    def on_post(self, req, resp):
        user = authenticate(req, resp)

        if not user:
            return

        post_id = req.media.get('postId')
        comment_id = req.media.get('commentId')  # Ignored because reporting is censorship in the first place.
        reason = req.media.get('reason')
        description = req.media.get('description')

        if not post_id:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Post id is not given.'}
            return

        if not reason:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Reason is not given.'}
            return

        try:
            reason = int(reason)
        except ValueError:
            resp.status = falcon.HTTP_400  # Bad request
            resp.media = {'message': 'Reason must be an integer.'}
            return

        post = POST_REPO.find_post(post_id)

        if not post:
            resp.status = falcon.HTTP_406  # Not acceptable
            resp.media = {'message': 'Post id does not exist.'}
            return

        if comment_id:
            resp.status = falcon.HTTP_200
            resp.media = {'message': 'Ignored'}
            return

        report = Report(reporting_user_id=user.get_public_id(), reported_user_id=post.get_user_id(), post_id=post_id,
                        reason=reason, description=description)

        post = POST_REPO.on_new_report(post, report)

        #  These two commands can be aggregated into one command.
        USER_REPO.update_user_post(post)
        USER_REPO.on_report_on_user(post.get_user_id(), report)

        USER_REPO.on_new_report(user, report)

        resp.status = falcon.HTTP_200
        resp.media = report.get_obj()


def setup(app, prefix):
    app.add_route(prefix, _())
