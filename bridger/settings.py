from typing import Dict, List

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.reverse import reverse

from .enums import AuthType


def jwt_auth(request: Request) -> Dict:
    return {
        "type": "JWT",
        "config": {
            "token": reverse("token_obtain_pair", request=request),
            "refresh": reverse("token_refresh", request=request),
            "verify": reverse("token_verify", request=request),
            "username_field_key": get_user_model().USERNAME_FIELD,
            "username_field_label": "Email",
        },
    }


def get_bridger_auth(request: Request, auth_type: AuthType = AuthType.JWT) -> Dict:
    auth_method = globals()[f"{auth_type.value.lower()}_auth"]
    return getattr(settings, "BRIDGER_AUTH", jwt_auth)(request)


def get_bridger_frontend_user_configuration_order() -> List:
    return getattr(
        settings, "BRIDGER_FRONTEND_USER_CONFIGURATION_ORDER", ["config__order"]
    )
