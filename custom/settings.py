# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CUSTOM_INSTALLED_APPS = (
    #'custom',
)
CUSTOM_TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'custom/templates'),
)
CUSTOM_STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'custom/static'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'startup',
        'USER': 'startup',
        'PASSWORD': 'startup',
        'HOST': ''
    }
}

LANGUAGES = (
    ('en', 'English'),
    ('th', 'Thai'),
)
LANGUAGE_CODE = 'en'
MODELTRANSLATION_LANGUAGES = ('th', 'en')
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

SEARCH_INDEX_NAME = 'startup'

STATIC_URL = '/static/'

SITE_NAME = 'new.set.or.th'
SITE_SLOGAN = "New Economic Warrior (NEW)'s platform"
DEFAULT_FROM_EMAIL = 'New Economic Warrior <no-reply@new.set.or.th>'
SITE_URL = 'https://new.set.or.th'
SITE_LOGO_URL = '%simages/logo-startup.png' % STATIC_URL
SITE_FAVICON_URL = '%simages/favicon-startup.png' % STATIC_URL

GOOGLE_ANALYTICS_KEY = 'TODO: read from settings_local.py'

MAIN_DESCRIPTION = 'custom share description here'

ENABLE_SOCIAL_ENTERPRISE = False
ENABLE_STARTUP = True
ENABLE_SUMMARY = False
CURRENCY = 'THB'
CURRENCY_SHORT = '฿'
THANK_AFTER_CREATE = True

ALLOWED_CREATE_ORGANIZATION_WITHOUT_APPROVAL = True
DEFAULT_TYPE_RECEIVER = 'startup'
DEFAULT_COUNTRY = 6
HIDE_COUNTRY = True
HIDE_FULL_PROFILE = True
HIDE_FOLLOWING = True
HIDE_TESTIMONIAL = True
HIDE_ADVANCE_PROFILE = True

LIST_PAGE_REDIRECT = 'presentation_role_list_browse'


# FEATURE
feature_now = datetime.now() + timedelta(hours=7) + timedelta(hours=4)
#feature_now += timedelta(hours=13)

FEATURE_TEMPLATE = 'feature/startup.html'
FEATURE_CSS_TEMPLATE = 'feature/startup_css.html'

def feature_enable():
    return  (datetime(2016, 4, 28, 9, 15) < feature_now < datetime(2016, 4, 28, 17, 0)) or \
            (datetime(2016, 4, 29, 9, 15) < feature_now < datetime(2016, 4, 29, 17, 0)) or \
            (datetime(2016, 4, 30, 9, 15) < feature_now < datetime(2016, 4, 30, 17, 0)) or \
            (datetime(2016, 5,  1, 9, 15) < feature_now < datetime(2016, 5,  1, 17, 0))



from filter import FILTER
from point import POINT
