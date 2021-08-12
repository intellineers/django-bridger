from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

@database_sync_to_async
def get_user(user_id):
    try:
        return get_user_model().objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """ Auth Middleware that authenticates a user with a JWT TOKEN """

    # def __init__(self, inner):
    #     self.inner = inner

    def populate_scope(self, scope):
        # Add it to the scope if it's not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        scope = dict(scope)
        # Scope injection/mutation per this middleware's needs.
        self.populate_scope(scope)
        try:
            jwt_access_token = scope["cookies"]["JWT-access"]
            UntypedToken(jwt_access_token)
            decoded_data = jwt_decode(jwt_access_token, settings.SECRET_KEY, algorithms=["HS256"])
            scope["user"] = await get_user(user_id=decoded_data["user_id"])
        except (InvalidToken, TokenError, KeyError):
            pass
        return await self.inner(scope, receive, send)
