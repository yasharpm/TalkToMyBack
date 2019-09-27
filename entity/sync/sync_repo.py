import pymongo

from entity.base_repo import BaseRepo
from entity.sync.sync import Sync
from entity.sync.sync_events import *
from entity.post.post import Post


class SyncRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, 'sync')

        self.db.create_index([(Sync.ACTOR_USER_ID, pymongo.HASHED)], name='actor_id')
        self.db.create_index([(Sync.AFFECTED_USER_ID, pymongo.HASHED)], name='affected_id')

    def new_post(self, post):
        post_obj = post.get_obj()

        user_id = bytes.fromhex(post_obj[Post.USER_ID])

        event = {
            Sync.EVENT_TYPE: EVENT_NEW_POST,
            Sync.ACTOR_USER_ID: user_id,
            Sync.AFFECTED_USER_ID: user_id,
            Sync.CONTENT: post.get_public_obj()
        }

        sync = Sync(event)

        result = self.db.insert_one(sync.get_obj())

        sync.set_mongo_id(result.inserted_id)

        return sync

    def new_view(self, actor, affected, post_id, views):
        event = {
            Sync.EVENT_TYPE: EVENT_NEW_VIEW,
            Sync.ACTOR_USER_ID: bytes.fromhex(actor),
            Sync.AFFECTED_USER_ID: bytes.fromhex(affected),
            Sync.CONTENT: {'postId': post_id, 'views': views}
        }

        sync = Sync(event)

        result = self.db.insert_one(sync.get_obj())

        sync.set_mongo_id(result.inserted_id)

        return sync

    def new_comment(self, actor, affected, comment):
        event = {
            Sync.EVENT_TYPE: EVENT_NEW_COMMENT,
            Sync.ACTOR_USER_ID: bytes.fromhex(actor),
            Sync.AFFECTED_USER_ID: bytes.fromhex(affected),
            Sync.CONTENT: comment.get_obj()
        }

        sync = Sync(event)

        result = self.db.insert_one(sync.get_obj())

        sync.set_mongo_id(result.inserted_id)

        return sync

    def new_like(self, actor, affected, like, liked):
        event = {
            Sync.EVENT_TYPE: EVENT_NEW_LIKE if liked else EVENT_REMOVED_LIKE,
            Sync.ACTOR_USER_ID: bytes.fromhex(actor),
            Sync.AFFECTED_USER_ID: bytes.fromhex(affected),
            Sync.CONTENT: like.get_obj()
        }

        sync = Sync(event)

        result = self.db.insert_one(sync.get_obj())

        sync.set_mongo_id(result.inserted_id)

        return sync
