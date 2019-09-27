import pymongo

from ttm_db import db
from entity.base_entity import BaseEntity


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseRepo(metaclass=Singleton):

    def __init__(self, repo_name):
        self.db = db[repo_name]
        self.db.create_index([(BaseEntity.ID, pymongo.HASHED)], name='entity_id')
        self.db.create_index([(BaseEntity.CREATED_TIME, pymongo.HASHED)], name='created_time')
        self.db.create_index([(BaseEntity.UPDATED_TIME, pymongo.HASHED)], name='updated_time')
