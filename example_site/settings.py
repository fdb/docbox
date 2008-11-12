import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'example.db'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

PROJECT_ROOT = os.path.dirname(__file__)
DOCBOX_ROOT = os.path.dirname(PROJECT_ROOT)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media'
ADMIN_MEDIA_PREFIX = '/media/admin/'

# The docbox module is in the parent folder.
sys.path.append(DOCBOX_ROOT)

# You must set this to let DocBox know where your documentation is.
DOCBOX_DOC_ROOT = os.path.join(DOCBOX_ROOT, 'docs')

SECRET_KEY = '<secret>'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'example_site.urls'

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)

# Include docbox in the list of installed applications.
INSTALLED_APPS = (
    'docbox',
)