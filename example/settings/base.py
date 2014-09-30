"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401
import os
import sys
import example as project_module
import inspect

#==============================================================================
# Generic Django project settings
#==============================================================================

ALLOWED_HOSTS = (
    '*',
    #'www.compute.amazonaws.com',
    #'compute.amazonaws.com',
    #'localhost',
)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

GRAPPELLI_ADMIN_TITLE = "Django Carbon Example"

SITE_ID = 1
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)
PAGE_LANGUAGES = (
    ('en-us', gettext_noop('US English')),
)

#==============================================================================
# Auth / security
#==============================================================================


AUTHENTICATION_BACKENDS += ()

SECRET_KEY = ':sdlk23j)SDS(&3g2a]dc08d923*^@)djJDD'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'south',
    'localflavor',

    #'storages',
    #'haystack',
    #'imagekit',
    #'registration', 
    'django-carbon.blog',
    'django-carbon.gallery',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    
    'django_extensions',
    'debug_toolbar',
    #'raven.contrib.django.raven_compat',

)

#==============================================================================
# Calculation of directories relative to the project module location
#==============================================================================

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
DATA_DIR = os.path.join(APP_DIR, 'data')
LIBS_DIR = os.path.join(APP_DIR, 'libs')
PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))
PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))

if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
        'activate_this.py')):
    VAR_ROOT = os.path.join(ve_path, 'var')
else:
    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)
#==============================================================================
# Project URLS and media settings
#==============================================================================
ROOT_URLCONF = 'example.urls'

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)



#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
    'example.kernel.context_processors.donottrack',
)


MIDDLEWARE_CLASSES += (
    "example.kernel.middleware.Django403Middleware",
    'example.kernel.middleware.DoNotTrackMiddleware',
)


#==============================================================================
# Third party app settings
#==============================================================================
AWS_ACCESS_KEY_ID       = ''
AWS_SECRET_ACCESS_KEY   = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT',
    'Cache-Control': 'max-age=86400',
}

#==============================================================================
# Auth / security
#==============================================================================


#==============================================================================
# email / smtp
#==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587


EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


DEFAULT_FROM_EMAIL = ''
DEFAULT_TO_EMAIL = ''

NEWSLETTER_CONFIRM_EMAIL = False

#Error and Broken Link Notifications
# MANAGERS = (
#     ('Name', 'email'),
# )
# ADMINS = (
#     ('Name', 'email'),
# )

#==============================================================================
# DJANGO-CARBON SETTINGS
#==============================================================================
TAG_MODEL = 'django-carbon.blog.Tag'
#AUTH_USER_MODEL = 'django.contrib.auth.models.User'


#==============================================================================
# APIS
#==============================================================================
INSTAGRAM_CLIENT_ID = ''
INSTAGRAM_SECRET_CLIENT_ID = ''

TWITTER_CLIENT_ID = ''
TWITTER_SECRET_CLIENT_ID = ''

FACEBOOK_CLIENT_ID = ''
FACEBOOK_SECRET_CLIENT_ID = ''



#==============================================================================
# Database
#==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django-carbon-example',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '',
#         'HOST': '',
#         'PORT': 5432,
#         'USER': '',
#         'PASSWORD': ''
#     }
# }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': '',
        'INDEX_NAME': '',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

