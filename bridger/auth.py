from datetime import timedelta
from typing import Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from rest_framework import authentication
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


def unauthenticated(request: Request) -> Dict:
    return {"type": None}


def jwt_auth(request: Request) -> Dict:
    user_model = get_user_model()
    username_field_key = user_model.USERNAME_FIELD
    username_field_label = user_model._meta.get_field(username_field_key).verbose_name

    access = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", timedelta(minutes=5))
    refresh = settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME", timedelta(days=1))

    return {
        "type": "JWT",
        "config": {
            "token": reverse("token_obtain_pair", request=request),
            "refresh": reverse("token_refresh", request=request),
            "verify": reverse("token_verify", request=request),
            "token_lifetime": {"access": access, "refresh": refresh},
            "username_field_key": username_field_key,
            "username_field_label": username_field_label,
        },
    }


class JWTCookieAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        try:
            jwt_access_token = request.COOKIES["JWT-access"]
            UntypedToken(jwt_access_token)
            decoded_data = jwt_decode(jwt_access_token, settings.SECRET_KEY, algorithms=["HS256"])
            user = get_user_model().objects.get(id=decoded_data["user_id"])
            return (user, None)
        except (InvalidToken, TokenError, KeyError, get_user_model().DoesNotExist):
            raise AuthenticationFailed("Authentication Failed.")
            return None
