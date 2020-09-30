import pymongo
import random
import collections

from entity.base_repo import BaseRepo
from entity.post.post import Post
from entity.user.user import User
from entity.like.like import Like
from entity.repositories import COMMUNITY_REPO
from entity.community.community_errors import *
import ttm_util

ONE_DAY = 1000 * 60 * 60 * 24

RANDOM_CASES = [
    (ONE_DAY, 0.3),
    (ONE_DAY * 3, 0.25),
    (ONE_DAY * 7, 0.2),
    (ONE_DAY * 30, 0.1),
    (ONE_DAY * 90, 0.1)
]

# RANDOM_CASES = [
#     (ONE_DAY * 10, 0.01),
#     (ONE_DAY * 20, 0.1),
#     (ONE_DAY * 4 * 365, 0.3)
# ]

TODAY_POSTS_AGE = ONE_DAY
RECENT_POSTS_AGE = TODAY_POSTS_AGE * 7
MID_RANGE_POSTS_AGE = RECENT_POSTS_AGE * 8


class PostRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, 'post')

        self.db.create_index([(Post.USER_ID, pymongo.HASHED)], name='user_id')
        self.db.create_index([(Post.LANGUAGE, pymongo.HASHED)], name='language')
        self.db.create_index([(Post.COUNTRY, pymongo.HASHED)], name='country')
        self.db.create_index([(Post.COMMUNITY, pymongo.HASHED)], name='community')
        self.db.create_index([(Post.VIEW_COUNT, pymongo.HASHED)], name='view_count')
        self.db.create_index([(Post.REPORT_COUNT, pymongo.HASHED)], name='report_count')

        #self.db.update_many({}, {"$set": {
        #        Post.COMMUNITY: COMMUNITY_REPO.get_public_community_number()
        #    }})

    def new_post(self, user, content, language, country, community):
        post = Post(
            user_id=user.get_public_id(),
            user_name=user.get_obj().get(User.NAME, None),
            user_anonymous=False,
            content=content,
            language=language,
            country=country,
            community=community
        )

        post_obj = post.get_obj()

        post_obj[Post.UTIL_POST_COUNT] = self.db.count()

        result = self.db.insert_one(post_obj)

        post.set_mongo_id(result.inserted_id)

        return post

    def random_posts(self, count, language, country, community, processed=True):
        match = {}

        if language:
            match[Post.LANGUAGE] = language

        if country:
            match[Post.COUNTRY] = country

        if not community:
            community = COMMUNITY_REPO.get_public_community_id()

        start, end = COMMUNITY_REPO.get_community_number_range(community)

        if start == COMMUNITY_DOES_NOT_EXIST:
            return COMMUNITY_DOES_NOT_EXIST

        match[Post.COMMUNITY] = {'$gte': start, '$lt': end}  # TODO ALSO RESET ALL PREEXISTING POSTS

        age_ranges, probabilities = self._make_age_ranges_and_probabilities(RANDOM_CASES)

        post_age_range_counts = collections.Counter(random.choices(age_ranges, probabilities, k=count))

        posts = []
        remaining_count = count

        for age_range in age_ranges:
            match[Post.CREATED_TIME] = {'$gt': age_range[0], '$lt': age_range[1]}

            if age_range == age_ranges[-1]:
                range_count = remaining_count
            else:
                range_count = post_age_range_counts.get(age_range, 0)

            range_posts = self._aggregate_posts(match, range_count, processed)

            remaining_count -= len(range_posts)

            posts.extend(range_posts)

        random.shuffle(posts)

        return posts

    def exhibition_posts(self, count, language, country, community, day, week, month):
        match = {}

        if language:
            match[Post.LANGUAGE] = language

        if country:
            match[Post.COUNTRY] = country

        if not community:
            community = COMMUNITY_REPO.get_public_community_id()

        start, end = COMMUNITY_REPO.get_community_number_range(community)

        if start == COMMUNITY_DOES_NOT_EXIST:
            return COMMUNITY_DOES_NOT_EXIST

        match[Post.COMMUNITY] = {'$gte': start, '$lt': end}

        random_cases = [
            (TODAY_POSTS_AGE, day / 100),
            (RECENT_POSTS_AGE, week / 100),
            (MID_RANGE_POSTS_AGE, month / 100)
        ]

        age_ranges, probabilities = self._make_age_ranges_and_probabilities(random_cases)

        post_age_range_counts = collections.Counter(random.choices(age_ranges, probabilities, k=count))

        posts = []
        remaining_count = count

        for age_range in age_ranges:
            match[Post.CREATED_TIME] = {'$gt': age_range[0], '$lt': age_range[1]}

            if age_range == age_ranges[-1]:
                range_count = remaining_count
            else:
                range_count = post_age_range_counts.get(age_range, 0)

            range_posts = self._aggregate_posts(match, range_count, True)

            remaining_count -= len(range_posts)

            posts.extend(range_posts)

        random.shuffle(posts)

        return posts

    def _make_age_ranges_and_probabilities(self, random_cases):
        age_ranges = []
        probabilities = []

        remaining_probability = 1

        now = ttm_util.now()
        current_time = now

        for random_case in random_cases:
            age, probability = random_case

            relative_age = age - (now - current_time)

            age_range = (current_time - relative_age, current_time)
            age_ranges.append(age_range)

            current_time = age_range[0]

            probabilities.append(probability)
            remaining_probability -= probability

        age_ranges.append((0, current_time))
        probabilities.append(remaining_probability)

        return age_ranges, probabilities

    def _aggregate_posts(self, match, count, processed):
        posts = []

        post_objs = self.db.aggregate([{'$match': match}, {'$sample': {'size': count}}])

        if processed:
            for post_obj in post_objs:
                posts.append(Post(companion=post_obj).get_public_obj())
        else:
            for post_obj in post_objs:
                posts.append(Post(companion=post_obj))

        return posts

    def on_post_viewed(self, post_id, view_count):
        post = self.find_post(post_id)

        if not post:
            return None

        post.on_updated()

        post_obj = post.get_obj()

        post_obj[Post.VIEW_COUNT] += view_count

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.VIEW_COUNT: post_obj[Post.VIEW_COUNT],
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post

    def on_new_comment(self, comment):
        post = self.find_post(comment.get_post_id())

        if not post:
            return None

        post.on_updated()

        post_obj = post.get_obj()

        post_obj[Post.COMMENTS].insert(0, comment.get_obj())
        post_obj[Post.COMMENT_COUNT] += 1

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.COMMENT_COUNT: post_obj[Post.COMMENT_COUNT],
                Post.COMMENTS: post_obj[Post.COMMENTS],
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post

    def on_new_like(self, like, liked):
        post = self.find_post(like.get_post_id())

        if not post:
            return None, False

        post.on_updated()

        post_obj = post.get_obj()

        likes = post_obj[Post.LIKES]

        user_id = like.get_user_id()

        index = next((index for (index, like_obj) in enumerate(likes) if like_obj[Like.USER_ID] == user_id), -1)

        if index >= 0:
            if liked:
                #  Already liked
                return post, False
            else:
                likes.pop(index)
        else:
            if liked:
                likes.insert(0, like.get_obj())
            else:
                #  Already not liked
                return post, False

        post_obj[Post.LIKE_COUNT] = len(likes)

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.LIKE_COUNT: post_obj[Post.LIKE_COUNT],
                Post.LIKES: likes,
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post, True

    def find_post(self, post_id):
        post_id = bytes.fromhex(post_id)

        post_obj = self.db.find_one({Post.ID: post_id})

        if not post_obj:
            return None

        post = Post(companion=post_obj)

        return post

    def on_new_report(self, post, report):
        post.on_updated()

        post_obj = post.get_obj()

        post_obj[Post.REPORTS].insert(0, report.get_obj())
        post_obj[Post.REPORT_COUNT] += 1

        self.db.update_one(
            {Post.MONGO_ID: post_obj[Post.MONGO_ID]},
            {"$set": {
                Post.REPORT_COUNT: post_obj[Post.REPORT_COUNT],
                Post.REPORTS: post_obj[Post.REPORTS],
                Post.UPDATED_TIME: post_obj[Post.UPDATED_TIME]
            }}
        )

        return post

    def on_user_name_changed(self, user_public_id, user_name):
        self.db.update_many(
            {Post.USER_ID: user_public_id},
            {"$set": {
                Post.USER_NAME: user_name
            }}
        )
