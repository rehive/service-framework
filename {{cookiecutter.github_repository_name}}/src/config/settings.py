"""
For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os

from .plugins.sentry import *
from .plugins.secrets import *
from .plugins.rest_framework import *
from .plugins.yasg import *
from .plugins.database import *
from .plugins.gcloud_bucket import *
from .plugins.healthz import *

# Project paths
# ---------------------------------------------------------------------------------------------------------------------#
# Build paths inside the project like this: os.path.join(PROJECT_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']

# Installed apps
# ---------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sites',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

    '{{cookiecutter.module_name}}',

    'debug_toolbar',
    'drf_yasg',
    'healthz',
    'drf_rehive_extras',
    'django_rehive_extras',
    'storages',
]

# Middleware
# ---------------------------------------------------------------------------------------------------------------------

MIDDLEWARE = [
    'healthz.middleware.HealthCheckMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

if os.environ.get('GCLOUD_USE_STATIC', '') == 'True':
    STATIC_URL = 'https://storage.googleapis.com/' + os.environ.get('GCLOUD_STATIC_BUCKET') + '/'

# STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'var/www/static')

STATICFILES_DIRS = [
    # os.path.join(PROJECT_DIR, "var/www/static"),
    # '/var/www/static/',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'var/www/media')


# Template files
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/howto/static-files/

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
        'DIRS': [
            os.path.join(PROJECT_DIR, 'config/templates'),
        ],
    },
]

# Other
# ---------------------------------------------------------------------------------------------------------------------
VERSION = '1.0.0'

SITE_ID = 1

FIXTURE_DIRS = ['config/fixtures']

CACHE_DIR = os.path.join(PROJECT_DIR, 'var/cache')

# Logging
# ----------------------------------------------------------------------------------------------------------------------

from django.utils.log import DEFAULT_LOGGING

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    "loggers": {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
}