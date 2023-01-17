"""
fakester Django settings.
"""
from pathlib import Path

from decouple import config
from dj_database_url import parse as db_url

SRC_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SRC_DIR.parent

SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-y+rcy_fkylgf*=h5iu%a3hijnfwj)kx=a)-!$(+!gz_t4cr!7j",
)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost, 127.0.0.1, 0.0.0.0",
    cast=lambda hosts: [s.strip() for s in hosts.split(",")],
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
    # Third party
    "bootstrap3",
    "captcha",
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

WSGI_APPLICATION = "fakester.wsgi.application"

DATABASES = {
    "default": config(
        "DATABASE_URL",
        default="postgres://localhost/fakester",
        cast=db_url,
    ),
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

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "index"

##########
# Custom #
##########
AVAILABLE_DOMAINS = (
    "badsoftware.review",
    "doubledouce.club",
    "farnsworth.science",
    "forgettable.men",
    "momcorp.science",
    "mortifex.tech",
    "notarickyroll.website",
    "notarobot.date",
    "notbigon.faith",
    "realshark.loan",
    "sugarlumps.trade",
    "totallyreal.accountant",
)


###############
# Third-party #
###############

# django-recaptcha
RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY", default="")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY", default="")
