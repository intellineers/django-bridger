import logging
import os
from typing import Dict, List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from markdown.extensions.tables import TableExtension
from markdown_blockdiag import BlockdiagExtension
from rest_framework.request import Request
from rest_framework.reverse import reverse

from bridger.fsm.markdown_extensions import FSMExtension

logger = logging.getLogger(__name__)

DEFAULTS = {
    "PROFILE": "bridger.profile.default_profile",
    "DEFAULT_FRONTEND_USER_CONFIGURATION_ORDER": ["config__order"],
    "DEFAULT_AUTH_CONFIG": "bridger.auth.jwt_auth",
    "DEFAULT_NOTIFICATION_CONFIG": "bridger.notifications.settings.notification_config",
    "DEFAULT_SHARE_BUTTON": "bridger.share.buttons.share_action_button",
    "DEFAULT_SHARE_NOTIFICATION": "bridger.share.notifications.share_notification",
    "DEFAULT_SHARE_SERIALIZER": "bridger.share.serializers.ShareSerializer",
    "DEFAULT_USER_NAME": "bridger.views.get_user_name",
    "DEFAULT_MARKDOWN_EXTENSIONS": [TableExtension(), FSMExtension(), BlockdiagExtension(format="svg"),],
    "ADDITIONAL_DEFAUL_MODELVIEW_ATTRIBUTES": [],
    "FRONTEND_TEMPLATE": "bridger/frontend.html",
    "FRONTEND_CONTEXT": {
        "TITLE": "Workbench",
        "FONT_URL": "https://fonts.googleapis.com/css?family=Roboto:400,400i,500,500i,700,900&display=swap",
        "CDN_URLS": [
            "https://cdn.plot.ly/plotly-latest.min.js",
            "https://unpkg.com/react@16/umd/react.production.min.js",
            "https://unpkg.com/react-dom@16/umd/react-dom.production.min.js",
        ],
        "FAVICON_URL": None,
        "CSS_URL": None,
        "CONFIG_URL": None,
        "JS_URL": None,
    },
    "FRONTEND_MENU_CALENDAR": None,
    "MARKDOWN_TEMPLATE_TAGS": [],
    "CLUBHOUSE_CONFIG": "bridger.clubhouse.config",
    "CLUBHOUSE_API_TOKEN": os.environ.get("CLUBHOUSE_API_TOKEN", ""),
    "CLUBHOUSE_PROJECT_ID": os.environ.get("CLUBHOUSE_PROJECT_ID", ""),
}

IMPORT_STRINGS = [
    "PROFILE",
    "DEFAULT_AUTH_CONFIG",
    "DEFAULT_NOTIFICATION_CONFIG",
    "DEFAULT_SHARE_BUTTON",
    "DEFAULT_SHARE_NOTIFICATION",
    "DEFAULT_SHARE_SERIALIZER",
    "DEFAULT_USER_NAME",
    "CLUBHOUSE_CONFIG",
]


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e,)
        raise ImportError(msg)


class BridgerSettings:
    """The settings, which is mostly taken from the settings module of Django Rest Framework"""

    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def settings(self):
        return getattr(settings, "BRIDGER_SETTINGS", {})

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid Bridger Settings: {attr}")

        val = self.settings.get(attr, self.defaults[attr])

        if isinstance(val, dict):
            self.defaults[attr].update(val)
            val = self.defaults[attr]

        if attr in self.import_strings:
            val = perform_import(val, attr)

        return val


bridger_settings = BridgerSettings(DEFAULTS, IMPORT_STRINGS)
