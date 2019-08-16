from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.template.loader import render_to_string
from account.functions import user_can_edit_check
from common.functions import get_success_message, camelcase_to_underscore
from party.models import Party
from relation.forms import ExperienceEditForm, ReceivedFundingEditForm, InviteTestifyEditForm
from relation.functions import experience_render_reference, received_funding_render_reference

from relation.models import UserExperienceOrganization, PartyReceivedFundingParty, PartyInviteTestifyParty, \
    PartyReceivedInvestingParty


@login_required
def experience_create(request, instance=None):

    # Config for reuse
    ModelClass = UserExperienceOrganization
    instance = instance or ModelClass()

    if request.method == 'POST':
        
        POST = request.POST.copy()
        if int(POST['start_date_year']) and int(POST['start_date_month']) and not int(POST['start_date_day']):
            POST['start_date_day'] = 1
        if int(POST['end_date_year']) and int(POST['end_date_month']) and not int(POST['end_date_day']):
            POST['end_date_day'] =  1

        form = ExperienceEditForm(instance, ModelClass, request.user, POST)

        is_new = form.is_new()

        if form.is_valid():

            instance.dst = form.cleaned_data['dst']
            instance.title = form.cleaned_data['title']
            instance.description = form.cleaned_data['description']
            instance.start_date = form.cleaned_data['start_date']
            instance.end_date = form.cleaned_data['end_date']

            instance.save()


            message_success = get_success_message()

            if request.GET.get('_popup'):
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, experience_render_reference(instance).replace("'", "\\'"))

            messages.success(request, message_success)

            return redirect('%s_edit' % camelcase_to_underscore(instance.__class__.__name__), instance.id)

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')


    else:
        initial = {
            'title': instance.title,
            'description': instance.description,
            'start_date': instance.start_date,
            'end_date': instance.end_date
        }

        if instance.id:
            #initial['src'] = instance.src
            initial['dst'] = instance.dst


        form = ExperienceEditForm(instance, ModelClass, request.user, initial=initial)


    return render(request, 'relation/experience/form.html', {
        'form': form,
    })


@login_required
def experience_edit(request, experience_id):

    instance = get_object_or_404(UserExperienceOrganization, id=experience_id)

    # Check permission
    # user_can_edit_check(request.user, instance)

    return experience_create(request, instance)


@login_required
def received_funding_create(request, instance=None):

    # Config for reuse
    win_name = request.GET.get('winName') or 'id_received_fundings'

    if 'invest' in win_name.lower():
        ModelClass = PartyReceivedInvestingParty
    else:
        ModelClass = PartyReceivedFundingParty

    instance = instance or ModelClass()


    if request.method == 'POST':

        POST = request.POST.copy()
        if int(POST['date_year']) and int(POST['date_month']) and not int(POST['date_day']):
            POST['date_day'] = 1

        form = ReceivedFundingEditForm(instance, ModelClass, request.user, POST)

        is_new = form.is_new()

        if form.is_valid():

            if 'receive' in win_name:
                instance.dst = form.cleaned_data['dst']
            else:
                instance.src = form.cleaned_data['dst']

            instance.title = form.cleaned_data['title']
            instance.date = form.cleaned_data['date']
            instance.money_amount = form.cleaned_data['money_amount']

            instance.save()


            message_success = get_success_message()


            if request.GET.get('_popup'):

                field_name = win_name.replace('id_', '')
                message_success = '<script type="text/javascript"> opener.dismissAddAnotherPopup(window, \'%s\', \'%s\'); </script>' % (instance.id, received_funding_render_reference(instance, field_name=field_name).replace("'", "\\'"))

            messages.success(request, message_success)


            return HttpResponseRedirect('%s?winName=%s' % (resolve_url('%s_edit' % camelcase_to_underscore(PartyReceivedFundingParty.__name__), instance.id), win_name))

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')


    else:
        initial = {
            'title': instance.title,
            'date': instance.date,
            'money_amount': instance.money_amount
        }

        if instance.id:
            #initial['src'] = instance.src

            if 'give' in win_name:
                initial['dst'] = instance.src
            else:
                initial['dst'] = instance.dst


        form = ReceivedFundingEditForm(instance, ModelClass, request.user, initial=initial)


    party_label = 'Organization'

    if 'give' in win_name:
        party_label = 'Recipient'
    elif 'fund' in win_name:
        party_label = 'Supporter'
    elif 'invest' in win_name:
        party_label = 'Investor'

    page_title = 'Funding Record'
    if 'invest' in win_name.lower():
        page_title = 'Investing Record'

    return render(request, 'relation/received_funding/form.html', {
        'form': form,
        'party_label': party_label,
        'page_title': page_title
    })


@login_required
def received_funding_edit(request, received_funding_id):

    win_name = request.GET.get('winName') or 'id_received_fundings'

    if 'invest' in win_name.lower():
        ModelClass = PartyReceivedInvestingParty
    else:
        ModelClass = PartyReceivedFundingParty

    instance = get_object_or_404(ModelClass, id=received_funding_id)

    # Check permission
    # user_can_edit_check(request.user, instance)

    return received_funding_create(request, instance)


@login_required
def invite_testify_create(request, party_id):

    ModelClass = PartyInviteTestifyParty
    instance = ModelClass()

    if request.method == 'POST':

        form = InviteTestifyEditForm(instance, ModelClass, request.user, request.POST)

        party = get_object_or_404(Party, id=party_id)

        if form.is_valid():

            message = form.cleaned_data['message']

            for receiver in form.cleaned_data['receivers']:

                instance, created = PartyInviteTestifyParty.objects.get_or_create(src=request.logged_in_party, dst=receiver, party=party, defaults={
                    'src': request.logged_in_party,
                    'dst': receiver,
                    'party': party,
                    'data': message
                })


            message_success = 'Your invites has been completed'

            messages.success(request, message_success)

            return HttpResponseRedirect(party.get_absolute_url())

        else:
            return HttpResponseRedirect(party.get_absolute_url()+'?invite_error=true')


    else:

        form = InviteTestifyEditForm(instance, ModelClass, request.user)

    csrf_token_value = request.COOKIES['csrftoken']
    return render_to_string('relation/invite_testify/form.html', {
        'form': form,
        'csrf_token_value': csrf_token_value,
        'party_id': party_id
    })

