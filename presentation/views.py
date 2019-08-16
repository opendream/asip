import json
import urllib
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.loading import get_model
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django_tables2 import RequestConfig

from account.functions import user_can_edit_check
from account.models import User
from common.constants import STATUS_PENDING, STATUS_DRAFT, STATUS_PUBLISHED, STATUS_REJECTED
from notification.models import Notification

from organization.models import Organization

# =============================
# Global
# =============================
from presentation.forms import QueueForm
from presentation.tables import OrganizationTable, SortableOrganizationTable, SortablePeopleTable
from relation.autocomplete_light_registry import OrganizationAutocomplete, UserAutocomplete
from relation.models import PartySupportParty, PartyInvestParty, PartyReceivedInvestingParty, PartyPartnerParty
from taxonomy.models import OrganizationRole, Country


@login_required
def presentation_delete(request, app_label, model_name, id):

    ModelClass = get_model(app_label=app_label, model_name=model_name)
    instance = get_object_or_404(ModelClass, id=id)

    # Check permission
    user_can_edit_check(request, instance)
    instance.delete()

    model_name_display = model_name
    if hasattr(ModelClass, 'REQUEST_VERB_DISPLAY'):
        model_name_display = ModelClass.REQUEST_VERB_DISPLAY.lower()

    messages.success(request, _('Your %s have been deleted.') % model_name_display)


    if request.GET.get('next'):
        if request.GET.get('next') == '.':
            next = request.META.get('HTTP_REFERER', '/')
        else:
            next = request.GET.get('next')
    else:
        next = reverse('home')

    return HttpResponseRedirect(next)




# =============================
# Home
# =============================
def get_summary():

    if not settings.ENABLE_SUMMARY:
        return {}

    return {
        'country': Country.objects.all().count(),
        'organization': {
            'social_enterprise': Organization.objects.filter(
                type_of_organization=Organization.TYPE_SOCIAL_ENTERPRISE, status=STATUS_PUBLISHED).count(),
            'startup': Organization.objects.filter(
                type_of_organization=Organization.TYPE_STARTUP, status=STATUS_PUBLISHED).count(),
            Organization.TYPE_SUPPORTING_ORGANIZATION: Organization.objects.filter(
                type_of_organization=Organization.TYPE_SUPPORTING_ORGANIZATION, status=STATUS_PUBLISHED).count(),
        },
        'partysupportparty': PartySupportParty.objects.filter().count(),
        # 'partysupportparty': PartyReceivedFundingParty.objects.filter().count(),
        'partyinvestparty': PartyInvestParty.objects.filter().count(),
        'partyfundparty': PartyReceivedInvestingParty.objects.filter().count(),
        'partypartnerparty': PartyPartnerParty.objects.filter().count(),
        'type_of_need': {
            'through': Organization.type_of_needs.through.objects.filter(organization__status=1).count()
        },
        'happening': Notification.objects.filter(is_system=True, verb__isnull=False).exclude(
            status=STATUS_REJECTED).count()

    }

def home(request, force=False):
    if not force and settings.LANDING_PAGE_ENABLED:
        return render(request, 'presentation/landingpage.html', {'summary': get_summary()})
    else:

        return render(request, 'presentation/home.html', {
            'summary': get_summary()
        })

def about(request):
    return render(request, 'presentation/about.html')

def term(request):
    return render(request, 'presentation/term.html')

def privacy(request):
    return render(request, 'presentation/privacy.html')

def contact(request):
    return render(request, 'presentation/contact.html')

def search(request):

    if request.GET.get('ajax'):
        query = request.GET.dict()
        del query['ajax']
        return HttpResponseRedirect(reverse('search') + '#?' + urllib.urlencode(query))

    return render(request, 'search/index.html', {
        'query': json.dumps(request.GET)
    })

@login_required
def message_list(request):
    return render(request, 'message/list.html')


def presentation_role_list_redirect(request, role_permalink):
    return redirect(settings.LIST_PAGE_REDIRECT, role_permalink)

def presentation_role_list_browse(request, role_permalink):

    return render(request, 'party/list.html', {'role_permalink': role_permalink})

def presentation_role_list_happening(request, role_permalink):
    return render(request, 'party/happening.html', {'role_permalink': role_permalink})

# =============================
# Manage
# =============================

@login_required
def manage(request):
    raise Http404('No Implement Yet.')


def sortable_update(request, Inst, redirect_url_name, redirect_args=[], queue_form_params=None):

    if request.POST.get('adds') and queue_form_params:

        queue_form_params['data'] = request.POST
        form = QueueForm(**queue_form_params)

        if form.is_valid():
            for item in form.cleaned_data['adds']:
                item.promote = True
                item.save()

            messages.success(request, _('Your %s settings have been updated.') % _('list'))

    else:

        for (name, value) in request.POST.items():
            try:
                id = int(name.replace('priority-id-', ''))
                priority = int(value)
                inst = Inst.objects.get(id=id)

                if not inst.promote:
                    continue

                inst.priority = priority

                try:
                    inst.save(not_changed=True)
                except TypeError:
                    inst.save()

            except ValueError:
                pass

            try:
                id = int(name.replace('promote-id-', ''))
                print id
                promote = int(value)
                inst = Inst.objects.get(id=id)
                inst.promote = False
                inst.priority = 0

                try:
                    inst.save(not_changed=True)
                except TypeError:
                    inst.save()

            except ValueError:
                pass

        messages.success(request, _('Your %s settings have been updated.') % _('ordering'))


    return redirect(redirect_url_name, *redirect_args)


@staff_member_required
def manage_pending_organization(request, type_of_organization):

    item_list = Organization.objects\
        .filter(type_of_organization=type_of_organization, status=STATUS_PENDING)\
        .exclude(status=STATUS_DRAFT)\
        .order_by('created')

    q = request.GET.get('q')
    if q:
        item_list = item_list.filter(name__icontains=q.lower())

    table = OrganizationTable(item_list)
    RequestConfig(request).configure(table)

    return render(request, 'manage.html', {
        'table': table,
        'page_title': _('Manage Pending %s') % type_of_organization.title()
    })


@staff_member_required
def manage_promote_organization(request, type_of_organization):



    item_list = Organization.objects\
        .filter(type_of_organization=type_of_organization, promote=True) \
        .exclude(status=STATUS_DRAFT)\
        .order_by('-priority', '-created', '-id')

    table = SortableOrganizationTable(item_list)
    RequestConfig(request).configure(table)

    queue_form_params = {
        'queryset': Organization.objects.filter(type_of_organization=type_of_organization).exclude(Q(status=STATUS_DRAFT)|Q(promote=True)).order_by('name'),
        'autocomplete': OrganizationAutocomplete,
        'label': _('Choose promote %s') % type_of_organization.lower(),
        'placeholder': _('Type for search %s') % type_of_organization.lower(),
    }
    queue_form = QueueForm(**queue_form_params)

    if request.method == 'POST':
        return sortable_update(request, Organization, 'manage_promote_organization', redirect_args=[type_of_organization], queue_form_params=queue_form_params)


    return render(request, 'manage.html', {
        'queue_form': queue_form,
        'sortable': True,
        'table': table,
        'page_title': _('Promote %s') % type_of_organization
    })


@staff_member_required
def manage_promote_people(request):

    title = 'People'

    item_list = User.objects \
        .filter(promote=True, is_active=True) \
        .order_by('-priority', '-id')

    table = SortablePeopleTable(item_list)
    RequestConfig(request).configure(table)

    queue_form_params = {
        'queryset': User.objects.exclude(promote=True).order_by('first_name', 'last_name'),
        'autocomplete': UserAutocomplete,
        'label': _('Choose promote %s') % title.lower(),
        'placeholder': _('Type for search %s') % title.lower(),
    }
    queue_form = QueueForm(**queue_form_params)

    if request.method == 'POST':
        return sortable_update(request, User, 'manage_promote_people', queue_form_params=queue_form_params)

    return render(request, 'manage.html', {
        'queue_form': queue_form,
        'sortable': True,
        'table': table,
        'page_title': _('Promote %s') % title
    })


def handler403(request):
    return render(request, '403.html')

