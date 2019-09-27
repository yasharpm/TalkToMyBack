from entity.base_entity import BaseEntity


class Sync(BaseEntity):

    ACTOR_USER_ID = 'actor_user_id'
    AFFECTED_USER_ID = 'affected_user_id'
    EVENT_TYPE = 'event_type'
    CONTENT = 'content'

    def __init__(self, companion=None):
        if not companion:
            companion = {}

        BaseEntity.__init__(self, companion)

    def get_public_obj(self):
        public_obj = BaseEntity.get_public_obj(self)

        public_obj.pop(Sync.ACTOR_USER_ID, None)
        public_obj.pop(Sync.AFFECTED_USER_ID, None)
        public_obj.pop(Sync.UPDATED_TIME, None)

        return public_obj
