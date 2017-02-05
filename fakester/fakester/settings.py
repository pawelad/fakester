"""
Fakester application Django settings file

It uses `python-decouple` and `dj-database-url` libraries to get instance
specific config from '.env' file and environment variables
"""
from pathlib import Path

from decouple import config
from dj_database_url import parse as db_url


BASE_DIR = Path(__file__).parent.parent.parent
PROJECT_ROOT = Path(__file__).parent.parent


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost, 127.0.0.1',
    cast=lambda l: [s.strip() for s in l.split(',')],
)


ROOT_URLCONF = 'fakester.urls'

WSGI_APPLICATION = 'fakester.wsgi.application'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'fakester',
    'redirects',

    'bootstrap3',
    'captcha',
    'ratelimit',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             str(BASE_DIR.joinpath('fakester', 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + str(BASE_DIR.joinpath('db.sqlite3')),
        cast=db_url,
    )
}


MEDIA_URL = '/media/'
MEDIA_ROOT = str(PROJECT_ROOT.joinpath('media'))

STATIC_URL = '/static/'
STATIC_ROOT = str(PROJECT_ROOT.joinpath('staticfiles'))

STATICFILES_DIRS = [
    str(BASE_DIR.joinpath('fakester', 'static')),
]


LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Misc
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'index'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


#############################
# Third-party apps settings #
#############################

# django-recaptcha
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')


################
# Own settings #
################
AVAILABLE_DOMAINS = (
    'amishweekly.xyz',
    'deepersteeper.xyz',
    'estrogenesis.xyz',
    'funkinthetrunk.xyz',
    'fuzzfeet.xyz',
    'isitstd.xyz',
    'masterexploder.xyz',
    'momcorp.xyz',
    'mortifex.xyz',
    'mrmeeseeks.xyz',
    'notporn.xyz',
    'spottieottiedopaliscious.xyz',
    'thedeuce.xyz',
    'thefiggisagency.xyz',
    'theflabbergaster.xyz',
    'thekrappinger.xyz',
    'uphole.xyz',
)
