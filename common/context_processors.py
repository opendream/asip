import json
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from account.forms import EmailAuthenticationForm, AccountRegisterForm, ResetPasswordForm
from common.constants import STATUS_PENDING, STATUS_PUBLISHED, STATUS_DRAFT, STATUS_DELETED, STATUS_REJECTED
from organization.models import Organization
from party.models import Party
from relation.models import OrganizationHasPeople, UserApplyJob
from special.models import Special
from taxonomy.models import ArticleCategory, OrganizationRole

try:
    from asip.settings import feature_enable
except ImportError:
    pass

try:
    from custom.settings import feature_enable
except ImportError:
    pass

try:
    from asip.settings_local import feature_enable
except ImportError:
    pass

try:
    feature_enable
except NameError:
    def feature_enable():
        return False

def helper(request):


    try:
        logged_in_party = request.logged_in_party
    except TypeError:
        logged_in_party = 0

    nav_columns = 2
    nav_col1 = 0
    nav_col2 = 6
    nav_col3 = 6

    if request.user.is_staff:
        nav_columns = 3
        nav_col1 = 5
        nav_col2 = 4
        nav_col3 = 3


    special = request.GET.get('special')
    if special:

        if not request.session.get('has_session'):
            request.session['has_session'] = True

        request.session['special'] = special
        request.session.save()

    special = request.session.get('special', '')

    if special:
        try:
            special = Special.objects.get(permalink=special)
        except Special.DoesNotExist:
            pass

    required_organizations = []
    if request.user.is_authenticated():
        required_organizations = Organization.objects.filter(
            organization_has_people_src__dst=request.user,
            organization_has_people_src__src__admins=request.user,
            summary__isnull=True
        ).distinct()

    vary_print = request.GET.get('vary_print') or request.GET.get('print') or False
    vary_print = bool(vary_print)

    context = {
        'settings': settings,
        'request_popup': bool(request.GET.get('_popup') or request.POST.get('_popup')),
        'request_inline': bool(request.GET.get('_inline') or request.POST.get('_inline')),
        'request_pagination': request.GET.get('page'),
        'show_modal_login': request.user.is_anonymous() and request.path not in [reverse('account_login')],
        'show_modal_register': request.user.is_anonymous() and request.path not in [reverse('account_register')],
        'show_modal_password_reset': request.user.is_anonymous() and request.path not in [reverse('account_reset_password')],
        'show_modal_organizations': request.user.is_authenticated() and request.user.admins.all().count(),
        'login_form': AccountRegisterForm,
        'logged_in_party': logged_in_party,
        'password_reset_form': ResetPasswordForm,
        'BASE_URL': request.build_absolute_uri('/')[0:-1],
        'SITE_LOGO_URL': settings.SITE_LOGO_URL,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_SLOGAN': settings.SITE_SLOGAN,
        'SITE_FAVICON_URL': settings.SITE_FAVICON_URL,
        'STATUS_PUBLISHED': STATUS_PUBLISHED,
        'STATUS_PENDING': STATUS_PENDING,
        'STATUS_DRAFT': STATUS_DRAFT,
        'STATUS_DELETED': STATUS_DELETED,
        'STATUS_REJECTED': STATUS_REJECTED,
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
        'SITE_URL': settings.SITE_URL,
        'BASE_FRONT_URL': settings.BASE_FRONT_URL,

        'TYPE_SOCIAL_ENTERPRISE': Organization.TYPE_SOCIAL_ENTERPRISE,
        'TYPE_STARTUP': Organization.TYPE_STARTUP,
        'TYPE_SUPPORTING_ORGANIZATION': Organization.TYPE_SUPPORTING_ORGANIZATION,
        'TYPE_INVESTOR': Organization.TYPE_INVESTOR,
        'TYPE_CHOICES': Organization.TYPE_CHOICES,
        'EXPAND_TYPE_CHOICES': Organization.EXPAND_TYPE_CHOICES,
        'CURRENCY': settings.CURRENCY,
        'DEFAULT_TYPE_RECEIVER': settings.DEFAULT_TYPE_RECEIVER,
        'THANK_AFTER_CREATE':settings.THANK_AFTER_CREATE,

        'ALLOWED_CREATE_ORGANIZATION_WITHOUT_APPROVAL': settings.ALLOWED_CREATE_ORGANIZATION_WITHOUT_APPROVAL,

        'ARTICLE_CATEGORIES': ArticleCategory.objects.filter(level=0).order_by('id'),

        'nav_columns': nav_columns,
        'nav_col1': nav_col1,
        'nav_col2': nav_col2,
        'nav_col3': nav_col3,

        'HIDE_COUNTRY': settings.HIDE_COUNTRY,
        'HIDE_FULL_PROFILE': settings.HIDE_FULL_PROFILE,
        'HIDE_FOLLOWING': settings.HIDE_FOLLOWING,
        'HIDE_TESTIMONIAL': settings.HIDE_TESTIMONIAL,

        'DEBUG': int(settings.DEBUG),

        'party_list': Party.objects.all(),
        'organization_list': Organization.objects.all(),

        'admin_oroganization_list': Organization.objects.filter((Q(admins=request.user)|Q(created_by=request.user)) & Q(is_mockup=False)).distinct().extra(select={'is_published': 'status = %d' % STATUS_PUBLISHED, 'is_pending': 'status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending', '-status', 'id') if request.user.is_authenticated() else [],
        'admin_oroganization_mockup_list': Organization.objects.filter((Q(admins=request.user)|Q(created_by=request.user)) & Q(is_mockup=True)).distinct().extra(select={'is_published': 'status = %d' % STATUS_PUBLISHED, 'is_pending': 'status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending', '-status', 'id') if request.user.is_authenticated() else [],
        'admin_user_apply_job_exists': UserApplyJob.objects.filter(dst__admins=request.user).exists() if request.user.is_authenticated() else False,

        'feature_enable': feature_enable(),
        'special': special,
        'required_organizations': required_organizations,
        'organization_role_list': OrganizationRole.objects.all(),

        'vary_print': vary_print
    }

    return context
