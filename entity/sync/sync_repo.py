import pymongo

from entity.base_repo import BaseRepo
from entity.sync.sync import Sync
from entity.sync.sync_events import *
from entity.post.post import Post
from entity.user.user import User


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

    def sync(self, user, update_token, count):
        try:
            update_token = int(update_token)
        except TypeError or ValueError:
            update_token = 0

        affected_user_id = user.get_obj()[User.ID]

        last_sync_time = update_token

        query = {Sync.AFFECTED_USER_ID: affected_user_id, Sync.CREATED_TIME: {"$gt": last_sync_time}}

        raw_syncs = self.db.find(query).sort(Sync.CREATED_TIME).limit(count)

        syncs = []
        new_token = update_token

        for raw_sync in raw_syncs:
            sync = Sync(companion=raw_sync)

            syncs.append(sync.get_public_obj())

            new_token = raw_sync[Sync.CREATED_TIME]

        total_count = self.db.count_documents(query)
        has_more = total_count != len(syncs)

        return syncs, new_token, has_more
