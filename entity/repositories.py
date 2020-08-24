from entity.community.community_repo import CommunityRepo
COMMUNITY_REPO = CommunityRepo()

from entity.post.post_repo import PostRepo
POST_REPO = PostRepo()

from entity.user.user_repo import UserRepo
USER_REPO = UserRepo()

from entity.token.token_repo import TokenRepo
TOKEN_REPO = TokenRepo()

from entity.refresh_token.refresh_token_repo import RefreshTokenRepo
REFRESH_TOKEN_REPO = RefreshTokenRepo()

from entity.sync.sync_repo import SyncRepo
SYNC_REPO = SyncRepo()
