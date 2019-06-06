"""
Django settings for asip project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#BASE_PATH = os.path.abspath(os.path.dirname('.'))
#if 'collectstatic' in sys.argv:
#    BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TODO: read from settings_local.py'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True


# Application definition

INSTALLED_APPS = (
    'modeltranslation', # must be put before django.contrib.admin

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Library
    'django_extensions',
    'ckeditor',
    'sorl.thumbnail',
    'autocomplete_light',
    'activelink',
    'files_widget',
    'bootstrap3',
    'django_tables2',
    'compressor',
    'mptt',
    'social_auth',
    'tastypie',
    'haystack',
    'tagging',
    'import_export',
    'djcelery',

    # Project
    'presentation',
    'common',
    'taxonomy',
    'party',
    'account',
    'organization',
    'relation',
    'notification',
    'cms',
    'tagging_autocomplete_tagit',
    'multiselectfield',
    'feed',
    'special',
    'forum',

    # Log
    'opbeat.contrib.django',
)

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'account.middleware.AccountSocialAuthExceptionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'party.middleware.PartyMiddleware',

    #'common.middleware.CrawlerChecker',
    'common.middleware.ProtectApiScraper',
    'common.middleware.RequestProvider'

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',

    'common.context_processors.helper'
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'files_widget/templates'),
)

ROOT_URLCONF = 'asip.urls'

WSGI_APPLICATION = 'asip.wsgi.application'
ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'asip',
        'USER': 'asip',
        'PASSWORD': 'asip',
        'HOST': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGES = (
    ('en', 'English'),
)
LANGUAGE_CODE = 'en'
#MODELTRANSLATION_LANGUAGES = ('en')
#MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'sitestatic/')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'files_widget/static'),
)

AUTH_USER_MODEL = 'account.User'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',

    # TODO: Implement later
    #'social_auth.backends.twitter.TwitterBackend',

    'account.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

SESSION_COOKIE_AGE = 60*60*24

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Format'],
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Image', 'Table'],
            ['MediaEmbed']
        ],
        'width': 'auto',
        'height': '200',
        'format_tags': 'p;h3;h4;h5',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow,mediaembed',
        'forcePasteAsPlainText': True,
    },
    'minimal': {
        'toolbar': [
            ['Format'],
            ['Bold', 'Italic'],
            ['NumberedList', 'BulletedList'],
        ],
        'format_tags': 'p;h3;h4;h5',
        'width': 'auto',
        'height': '200',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow',
        'forcePasteAsPlainText': True,
    },
    'bold': {
        'toolbar': [
            ['Bold'],
        ],
        'width': 'auto',
        'height': '80',
        'autoGrow_minHeight': '80',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow',
        'forcePasteAsPlainText': True,
    },
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'mysite': {
            'level': 'WARNING',
            'handlers': ['opbeat'],
            'propagate': False,
        },
        # Log errors from the Opbeat module to the console (recommended)
        'opbeat.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

OPBEAT = {
    'ORGANIZATION_ID': '<ORGANIZATION-ID>',
    'APP_ID': '<APP-ID>',
    'SECRET_TOKEN': '<SECRET-TOKEN>',
}

import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'

THUMBNAIL_DEBUG = False
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_ENGINE = 'common.thumbnail.engines.common_engine.CommonEngine'


FILES_WIDGET_JQUERY_PATH = 'libs/jquery/jquery.min.js'
FILES_WIDGET_JQUERY_UI_PATH = 'libs/jquery-ui/js/jquery-ui-1.10.4.min.js'
FILES_WIDGET_TEMP_DIR = 'temp/files_widget/'
FILES_WIDGET_ADD_IMAGE_BY_URL = False

DEFAULT_IMAGE = '%simages/default.png' % STATIC_URL

TAGGING_AUTOCOMPLETE_JQUERY_UI_FILE = 'libs/jquery-ui/js/jquery-ui-1.10.4.min.js'
TAGGING_AUTOCOMPLETE_MAX_TAGS = 9999

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '%slibs/jquery/jquery.min.js' % STATIC_URL
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    },
}

SEARCH_INDEX_NAME = BASE_DIR.split('/')[-1] # /override/me/with/SEARCH_INDEX_NAME

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'search.backends.ConfigurableElasticSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': SEARCH_INDEX_NAME, # override at the bottom
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'search.signals.SearchRealtimeSignalProcessor'

# API
TASTYPIE_DEFAULT_FORMATS = ['json']

SHELL_PLUS = "ipython"

# CUSTOM ASIP PROJECT #############################

SITE_NAME = 'ImpactConnect.asia'
SITE_SLOGAN = 'Asian social investment portal'
DEFAULT_FROM_EMAIL = 'ImpactConnect <no-reply@impactconnect.asia>'
SITE_URL = 'http://impactconnect.asia'
SITE_LOGO_URL = '%simages/impactconnect-logo.png' % STATIC_URL
SITE_FAVICON_URL = '%simages/favicon.png' % STATIC_URL
SITE_LOGO_BUTTON_URL = '%simages/logo-button@2x.png' % STATIC_URL

MULTIPLE_COUNTRY = False

GOOGLE_ANALYTICS_KEY = ''

DISPLAY_UNPUBLISHED_HAPPENING = True

# DJANGO SOCIAL AUTH ##########################################################

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_SESSION_EXPIRATION = False
SOCIAL_AUTH_UUID_LENGTH = 22

FACEBOOK_APP_ID = 'TODO: read from settings_local.py'
FACEBOOK_API_SECRET = 'TODO: read from settings_local.py'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
FACEBOOK_EXTRA_DATA = [
    ('first_name-name', 'first_name'),
    ('last_name', 'last_name'),
    ('gender', 'gender'),
    ('link', 'facebook_url')
]

LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress']
LINKEDIN_CONSUMER_KEY = 'TODO: read from settings_local.py'
LINKEDIN_CONSUMER_SECRET = 'TODO: read from settings_local.py'
LINKEDIN_EXTRA_FIELD_SELECTORS = ['email-address', 'headline', 'industry', 'summary', 'public-profile-url', 'location', 'picture-url', 'picture-urls::(original)', 'positions']
LINKEDIN_EXTRA_DATA = [
    ('first-name', 'first_name'),
    ('last-name', 'last_name'),
    ('email-address', 'email'),
    ('headline', 'summary'),
    ('industry', 'occupation'),
    ('summary', 'description'),
    ('public-profile-url', 'linkedin_url'),

    ('location.name', 'country'),
    ('picture-urls.picture-url', 'image'),
    ('positions.position', 'experiences'),

]

FACEBOOK_PAGE_ID = ''
# Make sure is token never expire, let see http://stackoverflow.com/questions/17197970/facebook-permanent-page-access-token
FACEBOOK_PAGE_ACCESS_TOKEN = ''

#TWITTER_CONSUMER_KEY         = ''
#TWITTER_CONSUMER_SECRET      = ''


LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/account/error/'

SOCIAL_AUTH_USER_MODEL = 'account.User'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/account/error/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/account/redirect/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/account/redirect/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/account/redirect/'
SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'account.pipeline.generate_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'account.pipeline.update_user_details',
    'account.pipeline.update_profile',
)

RESERVED_USERNAMES = [
    'admin',
]

TASTYPIE_DEFAULT_FORMATS = ['json']

OWNER_URL_VIEWS = ['organization_detail', 'page_detail']

# OVERRIDE SETTINGS ###########################################################
try:
    import custom
    INSTALLED_APPS += ('custom', )
except ImportError:
    pass

CUSTOM_INSTALLED_APPS = ()
CUSTOM_TEMPLATE_DIRS = ()
CUSTOM_STATICFILES_DIRS = ()

LANDING_PAGE_ENABLED = False

CURRENCY = 'USD'
CURRENCY_SHORT = '$'

ALLOWED_CREATE_ORGANIZATION_WITHOUT_APPROVAL = False
THANK_AFTER_CREATE = False

DEFAULT_TYPE_RECEIVER = 'social-enterprise'
DEFAULT_COUNTRY = None
HIDE_COUNTRY = False
HIDE_FULL_PROFILE = False
HIDE_FOLLOWING = False
HIDE_TESTIMONIAL = False
HIDE_ADVANCE_PROFILE = False
MAIN_DESCRIPTION = ''

LIST_PAGE_REDIRECT = 'organization_role_list'

ENABLE_SOCIAL_ENTERPRISE = True
ENABLE_STARTUP = False
ENABLE_SUMMARY = True

try:
    from custom.settings import *
except ImportError:
    pass

try:
    from settings_local import *
except ImportError:
    pass

HAYSTACK_CONNECTIONS['default']['INDEX_NAME'] = SEARCH_INDEX_NAME

INSTALLED_APPS = INSTALLED_APPS + CUSTOM_INSTALLED_APPS
TEMPLATE_DIRS = CUSTOM_TEMPLATE_DIRS + TEMPLATE_DIRS
STATICFILES_DIRS = CUSTOM_STATICFILES_DIRS + STATICFILES_DIRS


# TESTING #####################################################################
if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
    MEDIA_URL = '/test_media/'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if 'runserver' in sys.argv:
    DEBUG = True


# DEBUG MODE ##################################################################

if DEBUG:
    #EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    COMPRESS_ENABLED = False
    GOOGLE_ANALYTICS_KEY = ''
