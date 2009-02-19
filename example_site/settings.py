import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(PROJECT_ROOT)
DOCBOX_ROOT = os.path.dirname(PROJECT_ROOT)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media'
ADMIN_MEDIA_PREFIX = '/media/admin/'

# The docbox module is in the parent folder.
sys.path.append(DOCBOX_ROOT)

# You must set this to let DocBox know where your documentation is.
DOCBOX_DOC_ROOT = os.path.join(DOCBOX_ROOT, 'docs')

DMIGRATIONS_DIR = os.path.join(PROJECT_ROOT, 'migrations')

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
    'docbox.mnml',
    'dmigrations',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
)

LOGIN_URL = '/login/'

def dependency_error(string):
    sys.stderr.write('%s\n' % string)
    sys.exit(1)

# Load local settings.  This can override anything in here, but at the very
# least it needs to define database connectivity.
try:
    from settings_local import *
except ImportError:
    dependency_error('Unable to read settings_local.py.')