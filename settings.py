# Django settings for allswingersclubs project.

APPEND_SLASH = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'clubs'             # Or path to database file if using sqlite3.
DATABASE_USER = 'clubs'             # Not used with sqlite3.
DATABASE_PASSWORD = 'clubs123'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9w+@byf8+ocnvn*!_n=@p4zhp#f-_5u#8r^8644)l3^^et4-7v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.common.CommonMiddleware',	
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	'django.middleware.cache.UpdateCacheMiddleware',
	'django.middleware.cache.FetchFromCacheMiddleware',
	# 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'allswingersclubs.urls'

TEMPLATE_DIRS = (
	# 'templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.flatpages',
    'django.contrib.admin',
	'django.contrib.sitemaps',
	'allswingersclubs.linkator',
	'allswingersclubs.directory',
	# 'debug_toolbar',
)

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
}

try:
	from local_settings import *
except ImportError:
	from production_settings import *