from django.conf import settings
from django.utils.translation import ugettext_lazy as _

STATUS_PUBLISHED = 1
STATUS_PENDING = -1
STATUS_DRAFT = 0
STATUS_DELETED = -2
STATUS_REJECTED = -3
STATUS_PROMOTE = 2


STATUS_CHOICES = (
    (STATUS_PUBLISHED, _('Published')),
    (STATUS_PENDING, _('Request for Approval')),
    (STATUS_DRAFT, _('Draft')),
)

STATUS_CHOICES_DISPLAY = (
    (STATUS_PUBLISHED, _('Published')),
    (STATUS_PENDING, _('Pending for Approval')),
    (STATUS_DRAFT, _('Draft')),
)

NO_IP = '127.0.0.1'

SHORT_UUID_ALPHABETS = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

SUMMARY_MAX_LENGTH = 80

TYPE_SOCIAL_ENTERPRISE = 'social-enterprise'
TYPE_STARTUP = 'startup'
TYPE_SUPPORTING_ORGANIZATION = 'supporter'
TYPE_INVESTOR = 'investor'
TYPE_PROGRAM = 'program'


TYPE_CHOICES = ()
EXPAND_TYPE_CHOICES = ()
if settings.ENABLE_SOCIAL_ENTERPRISE:
    TYPE_CHOICES += ((TYPE_SOCIAL_ENTERPRISE, _('Social Enterprise')), )
    EXPAND_TYPE_CHOICES += ((TYPE_SOCIAL_ENTERPRISE, _('Social Enterprise')), )

if settings.ENABLE_STARTUP:
    TYPE_CHOICES += ((TYPE_STARTUP, _('Startup')), )
    EXPAND_TYPE_CHOICES += ((TYPE_STARTUP, _('Startup')), )

# if settings.ENABLE_PROGRAM:
#     TYPE_CHOICES += ((TYPE_PROGRAM, _('Program')), )

TYPE_CHOICES += (
    (TYPE_INVESTOR, _('Investors')),
    (TYPE_SUPPORTING_ORGANIZATION, _('Supporter')),
    (TYPE_PROGRAM, _('Program'))
)
EXPAND_TYPE_CHOICES += (
    (TYPE_SUPPORTING_ORGANIZATION, _('Supporter')),
    (TYPE_INVESTOR, _('Investors')),
    (TYPE_PROGRAM, _('Program'))
)
