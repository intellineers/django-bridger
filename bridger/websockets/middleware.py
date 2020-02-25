from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


class JWTAuthMiddleware:
    """ Auth Middleware that authenticates a user with a JWT TOKEN """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # We should close all old connections here, somehow this bites itself with pytest
        # close_old_connections()

        try:
            jwt_access_token = scope["cookies"]["JWT-access"]
            UntypedToken(jwt_access_token)
        except (InvalidToken, TokenError, KeyError):
            return self.inner(dict(scope))
        else:
            decoded_data = jwt_decode(
                jwt_access_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = get_user_model().objects.get(id=decoded_data["user_id"])

        return self.inner(dict(scope, user=user))
