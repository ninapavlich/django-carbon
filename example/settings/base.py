"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401
import os
import sys
import example as project_module
import inspect

from example import env

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

# -- Server settings
if os.environ.get( 'ENVIRONMENT', 'local' ) != 'local':
    IS_ON_SERVER = True
else:
    IS_ON_SERVER = False

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
    # 'grappelli.dashboard',
    'grappelli',
    
    'localflavor',

    #'storages',
    #'haystack',
    'imagekit',
    #'robots',
    'ckeditor',
    'django_ace',

    'carbon.atoms',

    'carbon.compounds.core',
    'carbon.compounds.account',
    'carbon.compounds.media',
    'carbon.compounds.page',
    'carbon.compounds.portfolio',
    'carbon.compounds.clientset',

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
APPEND_SLASH = True

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
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "example.kernel.middleware.Django403Middleware",
    'example.kernel.middleware.DoNotTrackMiddleware',
)

# 'django.contrib.auth.middleware.AuthenticationMiddleware',
# 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',


#==============================================================================
# AWS
#==============================================================================
AWS_ACCESS_KEY_ID       = env.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY   = env.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'django-carbon'
AWS_STORAGE_BUCKET_NAME_MEDIA = 'django-carbon'
AWS_STATIC_FOLDER = 'static'
AWS_MEDIA_FOLDER = 'media'
AWS_S3_CUSTOM_DOMAIN    = '%s.s3.amazonaws.com'%(AWS_STORAGE_BUCKET_NAME)
AWS_S3_CUSTOM_DOMAIN_MEDIA    = '%s.s3.amazonaws.com'%(AWS_STORAGE_BUCKET_NAME_MEDIA)

AWS_STORAGE_BUCKET_NAME_MEDIA_SECURE = 'django-carbon-secure'
AWS_S3_CUSTOM_DOMAIN_MEDIA_SECURE    = '%s.s3.amazonaws.com'%(AWS_STORAGE_BUCKET_NAME_MEDIA_SECURE)


AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT',
    'Cache-Control': 'max-age=86400',
}

CKEDITOR_UPLOAD_PATH = "uploads/"

#==============================================================================
# Static Files
#==============================================================================
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'media'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

if IS_ON_SERVER:
    
    VAR_ROOT = '/srv/http/carbon_media'
    STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

    STATICFILES_STORAGE = 'example.s3utils.StaticRootS3BotoStorage'
    STATIC_URL = "//s3.amazonaws.com/%s/static/" % AWS_STORAGE_BUCKET_NAME

    AWS_S3_SECURE_URLS = True
    AWS_IS_GZIPPED = True

    GZIP_CONTENT_TYPES = (
        'text/css',
        'application/javascript',
        'application/x-javascript',
        'text/javascript',
    )

else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')  


CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 2 #only cache views for a few hours
CACHE_DURATION = 60 * 60 * 24 * 30    


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
#TAG_MODEL = 'django-carbon.blog.Tag'
AUTH_USER_MODEL = 'account.User'



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
        'NAME': os.path.join(VAR_ROOT, 'django-carbon-example'),
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


#==============================================================================
# CARBON SETTINGS
#==============================================================================
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
MEDIA_URL = '/uploads/'
MEDIA_MODEL = 'media.Media'
SECURE_MEDIA_MODEL = 'media.SecureMedia'
MEDIA_STORAGE = 'example.s3utils.MediaS3BotoStorage'
SECURE_MEDIA_STORAGE = 'example.s3utils.SecureMediaS3BotoStorage'


IMAGE_THUMBNAIL_WIDTH = 150
IMAGE_THUMBNAIL_HEIGHT = 150
IMAGE_THUMBNAIL_QUALITY = 80
IMAGE_MODEL = 'media.Image'
SECURE_IMAGE_MODEL = 'media.SecureImage'
IMAGE_STORAGE = 'example.s3utils.MediaS3BotoStorage'
SECURE_IMAGE_STORAGE = 'example.s3utils.SecureMediaS3BotoStorage'

TEMPLATE_MODEL = 'global.Template'