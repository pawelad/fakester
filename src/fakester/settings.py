"""fakester Django settings.

It uses `python-decouple` to load values from environment variables and a local
`.env` file (in that order). Custom and third party settings should be put in their
respective sections at the end of the file.
"""

from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from decouple import Choices, Csv, config
from dj_database_url import parse as db_url

from fakester import __version__

SRC_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SRC_DIR.parent

ENVIRONMENT = config(
    "ENVIRONMENT",
    default="local",
    cast=Choices(["local", "production"]),
)

SECRET_KEY = config("SECRET_KEY", default=None)
if not SECRET_KEY:
    if ENVIRONMENT == "local":
        SECRET_KEY = "CHANGE_ME"  # noqa
    else:
        raise ImproperlyConfigured(
            "You need to provide 'SECRET_KEY' when not running a local environment"
        )


DEBUG = config("DEBUG", default=False, cast=bool)
if DEBUG and ENVIRONMENT != "local":
    raise ImproperlyConfigured(
        "You need to disable 'DEBUG' when not running a local environment"
    )

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=None,
    cast=Csv(),
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Custom
    "fakester",
    "redirects",
    "utils",
    # Third party
    "crispy_bootstrap5",
    "crispy_forms",
    "django_ratelimit",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fakester.urls"

template_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
cached_template_loaders = [
    ("django.template.loaders.cached.Loader", template_loaders),
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": template_loaders if DEBUG else cached_template_loaders,
        },
    },
]

WSGI_APPLICATION = "fakester.wsgi.application"

DATABASES = {
    "default": config(
        "DATABASE_URL",
        default="postgres://postgres@localhost/fakester",
        cast=db_url,
    ),
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://localhost:6379"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

USE_TZ = True
TIME_ZONE = "UTC"

USE_I18N = False

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "admin:index"

# Needed for CSRF protection when running behind NGINX and Gunicorn
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

##########
# Custom #
##########
AVAILABLE_DOMAINS = config(
    "AVAILABLE_DOMAINS",
    default=None,
    cast=Csv(),
)

###############
# Third-party #
###############

# sentry-sdk
SENTRY_DSN = config("SENTRY_DSN", default=None)

if SENTRY_DSN:  # pragma: no cover
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        release=__version__,
        environment=ENVIRONMENT,
        send_default_pii=True,
        traces_sample_rate=1,
        profiles_sample_rate=0.5,
        ignore_errors=["DisallowedHost"],
    )

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
