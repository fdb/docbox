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
DOCBOX_ROOT = DOCBOX_PROJECTS_ROOT = os.path.dirname(PROJECT_ROOT)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
DOCBOX_MEDIA_ROOT = os.path.join(DOCBOX_ROOT, 'docbox', 'media')
DOCBOX_URL = ''
MEDIA_URL = '/media'
DOCBOX_MEDIA_URL = '/media/docbox'
ADMIN_MEDIA_PREFIX = '/media/admin/'

# The docbox module is in the parent folder.
sys.path.append(DOCBOX_ROOT)

# You must set this to let DocBox know where your documentation is.
DOCBOX_DOC_ROOT = os.path.join(DOCBOX_PROJECTS_ROOT, 'docs')
DOCBOX_SRC_ROOT = os.path.join(DOCBOX_PROJECTS_ROOT, 'src')
#sys.path.append(DOCBOX_SRC_ROOT)

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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'docbox.context_processors.url',
    'docbox.context_processors.media',
)

ROOT_URLCONF = 'example_site.urls'

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),
                 os.path.join(DOCBOX_ROOT, 'docbox', 'templates', 'docbox'))

# Include docbox in the list of installed applications.
INSTALLED_APPS = (
    'docbox',
    'docbox.mnml',
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