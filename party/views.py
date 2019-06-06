import bleach
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.functional import SimpleLazyObject
from account.functions import user_can_edit_check
from common.constants import STATUS_PUBLISHED
from common.functions import get_success_message, camelcase_to_underscore, underscore_to_camelcase
from party.forms import PortfolioEditForm
from party.functions import portfolio_render_reference
from party.middleware import get_logged_in_party
from party.models import Portfolio, Party


@login_required
def portfolio_create(request, instance=None):

    # Config for reuse
    ModelClass = Portfolio
    instance = instance or ModelClass()

    if request.method == 'POST':

        form = PortfolioEditForm(instance, ModelClass, request.user, request.POST)

        is_new = form.is_new()

        if form.is_valid():

            instance.title = form.cleaned_data['title']
            instance.description = form.cleaned_data['description']

            instance_images = instance._meta.get_field('images')
            if instance_images:
                instance_images.save_form_data(instance, form.cleaned_data['images'])

            instance.url = form.cleaned_data['url']

            instance.save()


            message_success = get_success_message(instance, is_new, [])

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, portfolio_render_reference(instance).replace("'", "\\'"))

            messages.success(request, message_success)

            return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')


    else:
        initial = {
            'title': instance.title,
            'description': instance.description,
            'images': instance.images,
            'url': instance.url,
        }


        form = PortfolioEditForm(instance, ModelClass, request.user, initial=initial)


    return render(request, 'party/portfolio/form.html', {
        'form': form,
    })


@login_required
def portfolio_edit(request, portfolio_id):

    instance = get_object_or_404(Portfolio, id=portfolio_id)

    # Check permission
    # user_can_edit_check(request.user, instance)

    return portfolio_create(request, instance)


def portfolio_detail(request, portfolio_id):

    return render(request, 'party/portfolio/detail.html', {
        'portfolio_id': portfolio_id
    })


@login_required
def party_activate(request, party_id=None):

    if party_id:
        party = get_object_or_404(Party, id=party_id)

        inst = party.get_inst()
        if hasattr(inst, 'status') and inst.status != STATUS_PUBLISHED:
            raise PermissionDenied()
        if hasattr(inst, 'is_active') and not inst.is_active:
            raise PermissionDenied()

        user_can_edit_check(request, party.get_inst())

        request.session['_logged_in_party_id'] = party.id
    else:
        request.session['_logged_in_party_id'] = None


    request.logged_in_party = SimpleLazyObject(lambda: get_logged_in_party(request))

    messages.success(request, 'Change your are "%s" success.' % bleach.clean(request.logged_in_party.get_display_name()))


    if request.GET.get('next'):
        next = request.GET.get('next')
    else:
        next = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(next)

@login_required
def party_deactivate(request):

    return party_activate(request)