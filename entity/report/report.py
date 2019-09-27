import uuid
import ttm_util


class Report:

    ID = 'id'
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'

    REPORTING_USER_ID = 'reporting_user_id'
    REPORTED_USER_ID = 'reported_user_id'
    POST_ID = 'post_id'
    REASON = 'reason'
    DESCRIPTION = 'description'

    def __init__(self, reporting_user_id=None, reported_user_id=None, post_id=None, reason=None, description=None,
                 companion=None):
        if not companion:
            companion = {}

        if reporting_user_id:
            companion[Report.REPORTING_USER_ID] = reporting_user_id

        if reported_user_id:
            companion[Report.REPORTED_USER_ID] = reported_user_id

        if post_id:
            companion[Report.POST_ID] = post_id

        if reason:
            companion[Report.REASON] = reason

        if description:
            companion[Report.DESCRIPTION] = description

        self.companion = companion

    def get_reporting_user_id(self):
        return self.get_obj()[Report.REPORTING_USER_ID]

    def get_post_id(self):
        return self.get_obj()[Report.POST_ID]

    def on_updated(self):
        self.get_obj()[Report.UPDATED_TIME] = ttm_util.now()

    def get_obj(self):
        if not self.companion.get(Report.CREATED_TIME):
            self.companion[Report.CREATED_TIME] = ttm_util.now()

        if not self.companion.get(Report.UPDATED_TIME):
            self.companion[Report.UPDATED_TIME] = self.companion[Report.CREATED_TIME]

        if not self.companion.get(Report.ID):
            self.companion[Report.ID] = uuid.uuid4().bytes.hex()

        return self.companion
