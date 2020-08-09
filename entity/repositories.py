from entity.token.token_repo import TokenRepo
from entity.refresh_token.refresh_token_repo import RefreshTokenRepo
from entity.user.user_repo import UserRepo
from entity.post.post_repo import PostRepo
from entity.sync.sync_repo import SyncRepo

TOKEN_REPO = TokenRepo()
REFRESH_TOKEN_REPO = RefreshTokenRepo()
USER_REPO = UserRepo()
POST_REPO = PostRepo()
SYNC_REPO = SyncRepo()
