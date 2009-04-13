import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

TIME_ZONE = 'America/Toronto'

LANGUAGE_CODE = 'en-ca'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, '../media/')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'caffette.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'ttc_tracker',
)

try:
    from settings_local import *
except ImportError:
    try:
        from mod_python import apache
        apache.log_error( "local settings not available", apache.APLOG_NOTICE )
    except ImportError:
        import sys
        sys.stderr.write( "local settings not available\n" )
