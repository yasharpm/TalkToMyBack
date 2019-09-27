import uuid
import ttm_util


class BaseEntity:

    MONGO_ID = '_id'
    ID = 'id'
    CREATED_TIME = 'created_time'
    UPDATED_TIME = 'updated_time'

    def __init__(self, companion=None):
        if not companion:
            companion = {}

        self.companion = companion

    def set_mongo_id(self, identifier):
        self.companion[BaseEntity.MONGO_ID] = identifier

    def get_mongo_id(self):
        return self.companion[BaseEntity.MONGO_ID]

    def on_updated(self):
        self.get_obj()[BaseEntity.UPDATED_TIME] = ttm_util.now()

    def get_obj(self):
        if not self.companion.get(BaseEntity.CREATED_TIME):
            self.companion[BaseEntity.CREATED_TIME] = ttm_util.now()

        if not self.companion.get(BaseEntity.UPDATED_TIME):
            self.companion[BaseEntity.UPDATED_TIME] = self.companion[BaseEntity.CREATED_TIME]

        if not self.companion.get(BaseEntity.ID):
            self.companion[BaseEntity.ID] = uuid.uuid4().bytes

        return self.companion

    def get_public_obj(self):
        obj = self.get_obj().copy()

        obj.pop(BaseEntity.MONGO_ID, None)

        if obj.get(BaseEntity.ID):
            obj[BaseEntity.ID] = self.get_public_id()

        return obj

    def get_public_id(self):
        obj = self.get_obj()

        return obj[BaseEntity.ID].hex()
