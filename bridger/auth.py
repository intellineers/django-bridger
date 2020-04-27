from typing import Dict

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.request import Request
from rest_framework.reverse import reverse


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
