import os
from datetime import timedelta

from decouple import config
from dj_database_url import parse as db_url
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = "bfeq_1i!f+0rmkkx6hfw#d4%t*!5t(3tv_lx0udc(!ebrr21vu"
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "channels",
    "bridger",
    "tests",
    "tests2",
    "corsheaders",
    "simple_history",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",  # Do i need this?
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer", "rest_framework.renderers.BrowsableAPIRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "bridger.permissions.RestAPIModelPermissions",
    ),
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z"
    # 'DEFAULT_METADATA_CLASS': 'wbutils.metadata.WorkbenchMetaData'
    # 'DEFAULT_METADATA_CLASS': 'drf_auto_endpoint.metadata.AutoMetadata'
}

CELERY_BROKER_URL = config("REDIS_URL", "redis://localhost:6379")
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"

CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": {"hosts": [("127.0.0.1", 6379)]},},
}

JWT_AUTH = {"JWT_AUTH_COOKIE": "JWT"}

SENDGRID_API_KEY = config("SENDGRID_API_KEY", default=None)

if SENDGRID_API_KEY:
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_HOST_USER = "apikey"
    EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tests.wsgi.application"
ASGI_APPLICATION = "tests.routing.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {"default": config("DATABASE_URL", cast=db_url)}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

TIME_ZONE = "Europe/Berlin"
USE_TZ = True

LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", None)
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", None)
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", None)
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL", None)
AWS_S3_SIGNATURE_VERSION = config("AWS_S3_SIGNATURE_VERSION", None)

AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)-8s[%(name)-12s][%(asctime)s]: %(message)s",
            "log_colors": {"DEBUG": "blue", "INFO": "white", "WARNING": "yellow", "ERROR": "red", "CRITICAL": "bold_red",},
        },
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "console"}},
    "loggers": {"": {"level": "INFO", "handlers": ["console"]}},
}

def frontend_menu_calendar(request):
    from rest_framework.reverse import reverse
    return reverse("calendar-list", request=request)

BRIDGER_SETTINGS = {
    "FRONTEND_CONTEXT": {
        "CSS_URL": "https://atonra-stainly-cdn.fra1.cdn.digitaloceanspaces.com/static/css/main-1-2-36-beta-2.css",
        "JS_URL": "https://atonra-stainly-cdn.fra1.cdn.digitaloceanspaces.com/static/js/main-1-2-36-beta-2.js",
    },
    "MARKDOWN_TEMPLATE_TAGS": ["test_tags"],
    "FRONTEND_MENU_CALENDAR": frontend_menu_calendar,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
}
