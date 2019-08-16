import json
import urllib
from urlparse import urlparse
import uuid
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, get_user_model, update_session_auth_hash, \
    REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset, password_reset_done
from django.core.urlresolvers import reverse
from django.db.models import QuerySet, FieldDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, render_to_response, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_decode, is_safe_url
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from social_auth.utils import backend_setting, setting
from social_auth.views import auth_complete, DEFAULT_REDIRECT, LOGIN_ERROR_URL, complete
from account.constants import PROMOTE_LIST_CONFIG, TAB_LIST_CONFIG, TAB_LIST_ROLE_CONFIG, PROMOTE_LIST_ROLE_CONFIG

from account.forms import EmailAuthenticationForm, ResetPasswordForm, AccountEditForm, InviteForm, AccountRegisterForm, \
    AppConnectForm
from account.functions import user_can_edit_check
from account.models import User, AppConnect
from api.resources import UserResource
from common.functions import staff_required, get_success_message, PermanentTokenGenerator
from organization.models import Organization
from party.models import Party
from party.views import party_activate
from relation.models import UserExperienceOrganization, PartyReceivedFundingParty, PartyReceivedInvestingParty, \
    PartySupportParty, PartyInvestParty, OrganizationHasPeople
from special.models import Special


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if False and not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def get_connect_token(app_id, user_id, virtual=False, raw=False):
    if virtual:
        token = '[new-token]'
    else:
        un = '%s--%s--%s' % (settings.SECRET_KEY, app_id, user_id)
        token = str(uuid.uuid5(uuid.NAMESPACE_DNS, un.encode('utf-8')))

    if raw:
        return token

    token = '%s--%s--%s' % (token, app_id, user_id)
    return token


def return_is_authenticated(request):
    if request.user.is_authenticated():

        redirect_to = request.GET.get('next') or reverse('home')

        if request.GET.get('new_app_id'):
            is_safe, app, allow_hosts = safe_app_redirect(request.GET.get('new_app_id'), redirect_to)

            if is_safe:

                token = get_connect_token(app.app_id, request.user.id)

                if '?' in redirect_to:
                    redirect_to = '%s&new_token=%s' % (redirect_to, token)
                else:
                    redirect_to = '%s?new_token=%s' % (redirect_to, token)

                return redirect(redirect_to)
            else:
                return render(request, 'account/app_connect_error.html', {
                    'message': 'The redirect uri <em>%s</em> does not allow, list of collected redirect uri below<br> %s' % (
                        redirect_to, ', '.join(allow_hosts))
                })
        else:
            return redirect(redirect_to)

    return False


def account_login(request):
    if request.method == 'POST' and not request.POST.get('remember_me', None): # No unit test
        request.session.set_expiry(0) # No unit test

    auth_result = return_is_authenticated(request)
    if auth_result:
        return auth_result

    return login(request, authentication_form=EmailAuthenticationForm,
        template_name='account/login.html')



def account_reset_password(request):
    if request.user.is_authenticated():
        return HttpResponse('access denied', status=403)

    redirect_url = request.GET.get('redirect')

    if redirect_url:
        token_generator = PermanentTokenGenerator()
    else:
        token_generator = default_token_generator

    goto = reverse('account_reset_password_done')
    if request.GET.get('new_app_id'):
        goto = '%s?new_app_id=%s' % (goto, request.GET.get('new_app_id'))

    return password_reset(request,
        token_generator=token_generator,
        template_name='account/password_reset_form.html',
        email_template_name='account/email/password_reset_email.html',
        subject_template_name='account/email/password_reset_email_subject.txt',
        password_reset_form=ResetPasswordForm,
        post_reset_redirect=goto,
    )


def account_reset_password_done(request):
    return password_reset_done(request,
        template_name='account/password_reset_done.html'
    )


def account_reset_password_confirm(request, uidb64=None, token=None, email_setting=False):

    if not request.GET.get('i_am_human'):
        return render(request, 'detect_human.html')

    UserModel = get_user_model()

    try:
        uid_int = urlsafe_base64_decode(uidb64)
        user = UserModel.objects.get(id=uid_int)
    except (ValueError, UserModel.DoesNotExist):
        user = None

    redirect_url = request.GET.get('redirect')

    if redirect_url:
        token_generator = PermanentTokenGenerator()
    else:
        token_generator = default_token_generator

    if user and token_generator.check_token(user, token):

        user.is_active = True
        user.save()

        user_authen = authenticate(username=user.username, ignore_password=True)
        auth_login(request, user_authen)

        if redirect_url:
            return redirect(redirect_url)

        if email_setting:
            return redirect(reverse('account_edit') + '?advance=1' + '##email-notification-settings')

        qs = request.GET.urlencode()
        if qs:
            qs = '&%s' % qs

        goto = reverse('account_edit') + '?reset_password=1' + qs

        return redirect(goto)
    else:
        return account_register_confirm_invalid(request, user, uidb64, token, email_setting=email_setting)



def account_settings_confirm(request, uidb64=None, token=None):
    return account_reset_password_confirm(request, uidb64, token, email_setting=True)


@login_required
def account_edit(request, people_id=None):
    required_password = request.GET.get('reset_password')
    required_job = request.GET.get('required_job')

    manage = request.GET.get('manage') and not required_password

    if people_id and request.user.is_staff:
        user_id = people_id
    elif not people_id:
        user_id = request.user.id
    else:
        user_id = people_id


    UserModel = get_user_model()
    user = UserModel.objects.get(id=user_id)

    required_complete_profile = user.user_roles.count() == 0


    # Check permission
    user_can_edit_check(request.user, user)

    if request.method == 'POST':
        form = AccountEditForm(user, UserModel, request.user, required_password, required_job, request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.gender = form.cleaned_data['gender']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.occupation = form.cleaned_data['occupation']
            user.summary = form.cleaned_data['summary']
            user.description = form.cleaned_data['description']
            user.skills = form.cleaned_data['skills']

            # User relation
            user.notification_allow_email_send_organizationhaspeople = form.cleaned_data['notification_allow_email_send_organizationhaspeople']
            user.notification_allow_email_send_partysupportparty = form.cleaned_data['notification_allow_email_send_partysupportparty']
            user.notification_allow_email_send_partyfollowparty = form.cleaned_data['notification_allow_email_send_partyfollowparty']
            user.notification_allow_email_send_partycontactparty = form.cleaned_data['notification_allow_email_send_partycontactparty']
            user.notification_allow_email_send_partytestifyparty = form.cleaned_data['notification_allow_email_send_partytestifyparty']
            user.notification_allow_email_send_partyinvitetestifyparty = form.cleaned_data['notification_allow_email_send_partyinvitetestifyparty']
            user.notification_allow_email_send_partylove = form.cleaned_data['notification_allow_email_send_partylove']
            # Organization relation
            user.notification_allow_email_send_organization_partypartnerparty = form.cleaned_data['notification_allow_email_send_organization_partypartnerparty']
            user.notification_allow_email_send_organization_userexperienceorganization = form.cleaned_data['notification_allow_email_send_organization_userexperienceorganization']
            user.notification_allow_email_send_organization_partysupportparty = form.cleaned_data['notification_allow_email_send_organization_partysupportparty']

            user.notification_allow_email_send_organization_partyfollowparty = form.cleaned_data['notification_allow_email_send_organization_partyfollowparty']
            user.notification_allow_email_send_organization_partycontactparty = form.cleaned_data['notification_allow_email_send_organization_partycontactparty']
            user.notification_allow_email_send_organization_partytestifyparty = form.cleaned_data['notification_allow_email_send_organization_partytestifyparty']
            user.notification_allow_email_send_organization_organizationparticipate = form.cleaned_data['notification_allow_email_send_organization_organizationparticipate']
            user.notification_allow_email_send_organization_partyinvitetestifyparty = form.cleaned_data['notification_allow_email_send_organization_partyinvitetestifyparty']
            user.notification_allow_email_send_organization_partylove = form.cleaned_data['notification_allow_email_send_organization_partylove']

            # Follower
            user.notification_allow_email_send_from_follow = form.cleaned_data['notification_allow_email_send_from_follow']

            user.facebook_url = form.cleaned_data['facebook_url']
            user.twitter_url = form.cleaned_data['twitter_url']
            user.linkedin_url = form.cleaned_data['linkedin_url']
            user.homepage_url = form.cleaned_data['homepage_url']

            # user.attachments = form.cleaned_data['attachments']

            user.job_email = form.cleaned_data['job_email']
            user.job_telephone = form.cleaned_data['job_telephone']

            instance_attachments = user._meta.get_field('attachments')
            if instance_attachments:
                instance_attachments.save_form_data(user, form.cleaned_data.get('attachments'))

            user.interests.clear()
            for interest in form.cleaned_data['interests']:
                user.interests.add(interest)

            user.user_roles.clear()
            for user_role in form.cleaned_data['user_roles']:
                user.user_roles.add(user_role)

            user.country = form.cleaned_data['country']

            # Use save_form_data like model form
            user_image = user._meta.get_field('image')

            if user_image:
                user_image.save_form_data(user, form.cleaned_data['image'])


            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)


            user.job_status = form.cleaned_data['job_status']
            user.job_public_status = {'True': True, 'False': False, '': None}[form.cleaned_data['job_public_status']]
            user.job_position = form.cleaned_data['job_position']
            user.money_salary = form.cleaned_data['money_salary']
            user.job_criteria = form.cleaned_data['job_criteria']

            user.job_roles.clear()
            for job_role in form.cleaned_data['job_roles']:
                user.job_roles.add(job_role)

            user.job_locations.clear()
            for job_location in form.cleaned_data['job_locations']:
                user.job_locations.add(job_location)

            user.save()

            OrganizationHasPeople.objects.filter(dst=user).exclude(src=form.cleaned_data['organizations']).delete()
            for organization in form.cleaned_data['organizations']:
                OrganizationHasPeople.objects.get_or_create(src=organization, dst=user)


            portfolios = [portfolio.id for portfolio in form.cleaned_data['portfolios']]
            user.portfolios.exclude(id__in=portfolios).delete()

            portfolios = [portfolio.id for portfolio in user.portfolios.all()]
            for portfolio in form.cleaned_data['portfolios'].exclude(id__in=portfolios):
                user.portfolios.add(portfolio)

            experience_list = [experience.id for experience in form.cleaned_data['experiences']]
            UserExperienceOrganization.objects.filter(src=user).exclude(id__in=experience_list).delete()
            for experience in form.cleaned_data['experiences']:
                if not experience.src:
                    experience.src = user
                    experience.save()


            PartySupportParty.objects.filter(src=user).exclude(dst=form.cleaned_data['recipients']).delete()
            for recipient in form.cleaned_data['recipients']:
                if user.id == recipient.id:
                    continue
                PartySupportParty.objects.get_or_create(src=user, dst=recipient)

            gived_fundings = [gived_funding.id for gived_funding in form.cleaned_data['gived_fundings']]
            PartyReceivedFundingParty.objects.filter(dst__id=user.id).exclude(id__in=gived_fundings).delete()
            for gived_funding in form.cleaned_data['gived_fundings']:
                if not gived_funding.dst:
                    gived_funding.dst = user.party_ptr
                    gived_funding.swap = True
                    gived_funding.save()


            PartyInvestParty.objects.filter(src=user).exclude(dst=form.cleaned_data['invest_recipients']).delete()
            for invest_recipient in form.cleaned_data['invest_recipients']:
                if user.id == invest_recipient.id:
                    continue
                PartyInvestParty.objects.get_or_create(src=user, dst=invest_recipient)

            gived_investings = [gived_investing.id for gived_investing in form.cleaned_data['gived_investings']]
            PartyReceivedInvestingParty.objects.filter(dst__id=user.id).exclude(id__in=gived_investings).delete()
            for gived_investing in form.cleaned_data['gived_investings']:
                if not gived_investing.dst:
                    gived_investing.dst = user.party_ptr
                    gived_investing.swap = True
                    gived_investing.save()

            if people_id:
                message_success = get_success_message(user, False, [])
                messages.success(request, message_success)
                return redirect('people_edit', people_id)
            else:
                messages.success(request, _(
                    'Your account profile have been updated. View your profile page <a href="%s">here</a>') % reverse(
                    'account'))
                #party_activate(request, user.id)

                next = request.GET.get('next')
                if next:
                    app_id = request.GET.get('new_app_id')
                    if app_id:
                        token = get_connect_token(app_id, request.user.id)
                        next = '%s?new_app_id=%s&new_token=%s' % (next, app_id, token)

                    return redirect(next)

                goto = reverse('account_edit')
                if request.GET.get('manage'):
                    goto = '%s?manage=1' % goto


                return redirect(goto)

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')

    else:

        email = user.email
        if email[0:7] == 'unknow.':
           email = ''

        username = user.username
        if username[0:7] == 'unknow.':
            username = ''
        

        initial = {
            'username': username,
            'email': email,
            'gender': user.gender,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'occupation': user.occupation,
            'summary': user.summary,
            'description': user.description,
            'facebook_url': user.facebook_url,
            'twitter_url': user.twitter_url,
            'linkedin_url': user.linkedin_url,
            'homepage_url': user.homepage_url,
            'image': user.image,
            'country': user.country,
            'skills': user.skills,
            'job_status': user.job_status,
            'job_public_status': user.job_public_status,
            'job_position': user.job_position,
            'money_salary': user.money_salary,
            'job_criteria': user.job_criteria,
            'job_email': user.job_email or user.email,
            'job_telephone': user.job_telephone,
            'attachments': user.attachments,
            'notification_allow_email_send_organizationhaspeople': user.notification_allow_email_send_organizationhaspeople,
            'notification_allow_email_send_partysupportparty': user.notification_allow_email_send_partysupportparty,
            'notification_allow_email_send_partyfollowparty': user.notification_allow_email_send_partyfollowparty,
            'notification_allow_email_send_partycontactparty': user.notification_allow_email_send_partycontactparty,
            'notification_allow_email_send_partytestifyparty': user.notification_allow_email_send_partytestifyparty,
            'notification_allow_email_send_partyinvitetestifyparty': user.notification_allow_email_send_partyinvitetestifyparty,
            'notification_allow_email_send_partylove': user.notification_allow_email_send_partylove,
            'notification_allow_email_send_organization_partypartnerparty': user.notification_allow_email_send_organization_partypartnerparty,
            'notification_allow_email_send_organization_userexperienceorganization': user.notification_allow_email_send_organization_userexperienceorganization,
            'notification_allow_email_send_organization_partysupportparty': user.notification_allow_email_send_organization_partysupportparty,
            'notification_allow_email_send_organization_partyfollowparty': user.notification_allow_email_send_organization_partyfollowparty,
            'notification_allow_email_send_organization_partycontactparty': user.notification_allow_email_send_organization_partycontactparty,
            'notification_allow_email_send_organization_partytestifyparty': user.notification_allow_email_send_organization_partytestifyparty,
            'notification_allow_email_send_organization_organizationparticipate': user.notification_allow_email_send_organization_organizationparticipate,
            'notification_allow_email_send_organization_partyinvitetestifyparty': user.notification_allow_email_send_organization_partyinvitetestifyparty,
            'notification_allow_email_send_organization_partylove': user.notification_allow_email_send_organization_partylove,
            'notification_allow_email_send_from_follow': user.notification_allow_email_send_from_follow
        }

        if user.id:
            initial['interests'] = user.interests.all()
            initial['user_roles'] = user.user_roles.all()
            initial['organizations'] = Organization.objects.filter(organization_has_people_src__dst=user).distinct()
            initial['portfolios'] = user.portfolios.all().distinct()
            initial['experiences'] = UserExperienceOrganization.objects.filter(src=user).distinct()


            initial['recipients'] = Party.objects.filter(support_dst__src=user).distinct()
            initial['gived_fundings'] = PartyReceivedFundingParty.objects.filter(dst__id=user.id).distinct()

            initial['invest_recipients'] = Party.objects.filter(invest_dst__src=user).distinct()
            initial['gived_investings'] = PartyReceivedInvestingParty.objects.filter(dst__id=user.id).distinct()

            initial['job_roles'] = user.job_roles.all()
            initial['job_locations'] = user.job_locations.all()





        special = request.session.get('special')
        if special:

            get_special = request.GET.get('special')


            if get_special and not required_complete_profile and user.specials.filter(permalink=get_special).count() > 0:
                return redirect('/%s/' % get_special)


            try:
                special = Special.objects.get(permalink=special)
                user.specials.add(special)
            except Special.DoesNotExist:
                pass

        msg_list = []

        if required_password:
            msg_list.append(_('Please, change your password'))

        if required_complete_profile:
            msg_list.append(_('Please, complete your profile "First name, Last name, Roles"'))

        if required_job and not (user.job_status and user.job_public_status is not None and user.job_position and user.money_salary and user.job_locations and user.job_criteria):
            msg_list.append(_('Please, complete your opportunities'))


        if len(msg_list) == 1:
            messages.error(request, '%s (check in red zone)' % msg_list[0])
        elif len(msg_list) > 1:
            msg_list.append('Check in red zone')
            messages.error(request, '<ul>%s</ul>' % ''.join(['<li>%s</li>' % m for m in msg_list]))

        form = AccountEditForm(user, UserModel, request.user, required_password, required_job, initial=initial)

        if manage:
            messages.success(request,
                "<script>setTimeout(function() {$('a[data-target=#modal-organizations]').click(); }, 2000);</script>" +
                'The link of your organizations will be appear on the '
                  '<b>Profile Menu</b> > <b>See All...</b>')
            return redirect('account_edit')

    return render(request, 'account/edit.html', {
        'form': form,
        'reset_password': required_password,
        'required_complete_profile': required_complete_profile,
        'required_job': required_job,
    })


@staff_member_required
def account_invite(request):

    if request.GET.get('success'):
        messages.success(request, _('The email invitation has been send.'))
        return redirect('account_invite')

    reeturn = password_reset(request,
        template_name='account/invite_form.html',
        email_template_name='account/email/invite_email.html',
        subject_template_name='account/email/invite_email_subject.txt',
        password_reset_form=InviteForm,
        post_reset_redirect='%s?success=1' % reverse('account_invite'),
    )



@csrf_protect
def inline_password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_context': extra_context
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)

            field_id = request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins'

            user = get_user_model().objects.get(email=form.cleaned_data['email'])
            return HttpResponseRedirect('%s&user_id=%s&field_id=%s' % (post_reset_redirect, user.id, field_id))
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def account_inline_invite(request):

    post_reset_redirect = '%s?success=1' % reverse('account_inline_invite')
    if request.GET.get('next'):
        post_reset_redirect = '%s&next=%s' % (post_reset_redirect, urllib.quote_plus(request.GET.get('next')))

    if request.GET.get('success'):

        messages.success(request, _('The email invitation has been send.'))
        return render(request, 'account/inline_invite_form.html', {
            'form': InviteForm(),
            'success': True,
            'user_id': request.GET.get('user_id'),
            'field_id': request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins',
            'create': request.POST.get('create') or request.GET.get('create') or False,
            'title': request.POST.get('title') or request.GET.get('title') or '',
            'manage': request.POST.get('manage') or request.GET.get('manage') or ''
        })

    return inline_password_reset(request,
        template_name='account/inline_invite_form.html',
        email_template_name='account/email/invite_email.html',
        subject_template_name='account/email/invite_email_subject.txt',
        password_reset_form=InviteForm,
        post_reset_redirect=post_reset_redirect,
        extra_context={
            'field_id': request.POST.get('field_id') or request.GET.get('field_id') or 'id_admins',
            'create': request.POST.get('create') or request.GET.get('create') or False,
            'title': request.POST.get('title') or request.GET.get('title') or '',
            'manage': request.POST.get('manage') or request.GET.get('manage') or ''
        }
    )



def account_register(request):

    auth_result = return_is_authenticated(request)
    if auth_result:
        return auth_result

    post_reset_redirect = '%s?success=1' % reverse('account_register')
    new_app_id = request.GET.get('new_app_id')
    next = request.GET.get('next')

    if new_app_id:
        post_reset_redirect = '%s&new_app_id=%s' % (post_reset_redirect, new_app_id)
    if next:
        post_reset_redirect = '%s&next=%s' % (post_reset_redirect, next)

    if request.GET.get('success'):
        messages.success(request, _('Please check your email account to verify your email and continue the registration process.'))
        goto = '%s?next=%s' % (reverse('account_register'), next)
        if new_app_id:
            token = get_connect_token(new_app_id, request.user.id)
            goto = '%s&new_app_id=%s' % (goto, new_app_id)
        return redirect(goto)

    return password_reset(request,
        template_name='account/register.html',
        email_template_name='account/email/register_email.html',
        subject_template_name='account/email/register_email_subject.txt',
        password_reset_form=AccountRegisterForm,
        post_reset_redirect=post_reset_redirect
    )


def account_register_confirm_invalid(request, user, uidb64, token, email_setting=False):
    if request.user.is_authenticated():
        messages.warning(request, _('You are logged in.'))
        return redirect('home')

    post_reset_redirect = '%s?success=1' % reverse('account_register_confirm', args=[uidb64, token])
    new_app_id = request.GET.get('new_app_id')
    next = request.GET.get('next')

    if new_app_id:
        post_reset_redirect = '%s&new_app_id=%s' % (post_reset_redirect, new_app_id)
    if next:
        post_reset_redirect = '%s&next=%s' % (post_reset_redirect, next)

    if request.GET.get('success'):
        messages.success(request, _('Please check your email account to verify your email and continue the registration process.'))

        goto = '%s?next=%s' % (reverse('account_register_confirm', args=[uidb64, token]), urllib.quote_plus(next))
        if new_app_id:
            goto = '%s&new_app_id=%s' % (goto, new_app_id)
        return redirect(goto)

    return password_reset(request,
        template_name='account/register_confirm_invalid.html',
        email_template_name='account/email/register_email.html',
        subject_template_name='account/email/register_email_subject.txt',
        password_reset_form=ResetPasswordForm,
        post_reset_redirect=post_reset_redirect,
        extra_context={'default_email': user.email}
    )


def account_register_confirm(request, uidb64=None, token=None, email_setting=False):

    if not request.GET.get('i_am_human'):
        return render(request, 'detect_human.html')

    UserModel = get_user_model()

    try:
        uid_int = urlsafe_base64_decode(uidb64)
        user = UserModel.objects.get(id=uid_int)
    except (ValueError, UserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()

        user_authen = authenticate(username=user.username, ignore_password=True)
        auth_login(request, user_authen)

        qs = request.GET.urlencode()
        if qs:
            qs = '&%s' % qs

        redirect_to = reverse('account_edit') + '?reset_password=1' + qs

        # if request.GET.get('new_app_id'):
        #     redirect_to = '%s&new_app_id=%s' % (redirect_to, urllib.quote_plus(request.GET.get('new_app_id')))
        # if request.GET.get('next'):
        #     redirect_to = '%s&next=%s' % (redirect_to, urllib.quote_plus(request.GET.get('next')))

        return redirect(redirect_to)
    else:
        return account_register_confirm_invalid(request, user, uidb64, token)


def account_logout(request, next_page=None,
                   template_name='registration/logged_out.html',
                   redirect_field_name=REDIRECT_FIELD_NAME,
                   current_app=None, extra_context=None):

    from django.contrib.auth.views import logout

    return logout(request, next_page=next_page, template_name=template_name, redirect_field_name=redirect_field_name,
                            current_app=current_app, extra_context=extra_context
    )

# =========================================================
# Social Auth
# =========================================================

def login_social(request, provider):

    next = request.GET.get('next')
    if next:

        app_id = request.GET.get('new_app_id')
        if app_id:
            request.session['social_new_app_id'] = app_id
            token = get_connect_token(app_id, '[user.id]', virtual=True)

            if '?' in next:
                next = '%s&new_token=%s' % (next, token)
            else:
                next = '%s?new_token=%s' % (next, token)

            request.GET = request.GET.copy()
            request.GET.update({'next': next})

        request.session['social_next'] = next

    from social_auth.views import auth
    return auth(request, provider)


def login_social_redirect(request):
    if request.GET.get('next'):
        url = request.GET.get('next')
    elif request.session.get('social_next'):
        url = request.session.get('social_next')
        request.session.delete('social_next')
    else:
        url = settings.LOGIN_REDIRECT_URL

    return redirect(url)



@login_required
def social_associate_complete(request, backend, *args, **kwargs):
    """Authentication complete process"""
    # pop redirect value before the session is trashed on login()
    redirect_value = request.session.get(REDIRECT_FIELD_NAME, '')
    user = auth_complete(request, backend, request.user, *args, **kwargs)

    if not user:
        url = backend_setting(backend, 'LOGIN_ERROR_URL', LOGIN_ERROR_URL)
    elif isinstance(user, HttpResponse):
        return user
    else:
        url = redirect_value or \
              backend_setting(backend,
                              'SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL') or \
              DEFAULT_REDIRECT
    return HttpResponseRedirect(url)



def social_complete_process(request, backend, *args, **kwargs):
    """Authentication complete process"""
    # pop redirect value before the session is trashed on login()
    redirect_value = request.session.get(REDIRECT_FIELD_NAME, '') or \
                     request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    user = auth_complete(request, backend, *args, **kwargs)

    if isinstance(user, HttpResponse):
        return user

    if not user and request.user.is_authenticated():
        return HttpResponseRedirect(redirect_value)

    msg = None
    if user:
        if getattr(user, 'is_active', True):
            # catch is_new flag before login() might reset the instance
            is_new = getattr(user, 'is_new', False)
            login(request, user)
            # user.social_user is the used UserSocialAuth instance defined
            # in authenticate process
            social_user = user.social_user
            if redirect_value:
                request.session[REDIRECT_FIELD_NAME] = redirect_value or \
                                                       DEFAULT_REDIRECT

            if setting('SOCIAL_AUTH_SESSION_EXPIRATION', True):
                # Set session expiration date if present and not disabled by
                # setting. Use last social-auth instance for current provider,
                # users can associate several accounts with a same provider.
                expiration = social_user.expiration_datetime()
                if expiration:
                    try:
                        request.session.set_expiry(expiration)
                    except OverflowError:
                        # Handle django time zone overflow, set default expiry.
                        request.session.set_expiry(None)

            # store last login backend name in session
            request.session['social_auth_last_login_backend'] = \
                    social_user.provider

            # Remove possible redirect URL from session, if this is a new
            # account, send him to the new-users-page if defined.
            new_user_redirect = backend_setting(backend,
                                           'SOCIAL_AUTH_NEW_USER_REDIRECT_URL')
            if new_user_redirect and is_new:
                url = new_user_redirect
            else:
                url = redirect_value or \
                      backend_setting(backend,
                                      'SOCIAL_AUTH_LOGIN_REDIRECT_URL') or \
                      DEFAULT_REDIRECT
        else:
            msg = setting('SOCIAL_AUTH_INACTIVE_USER_MESSAGE', None)
            url = backend_setting(backend, 'SOCIAL_AUTH_INACTIVE_USER_URL',
                                  LOGIN_ERROR_URL)
    else:
        msg = setting('LOGIN_ERROR_MESSAGE', None)
        url = backend_setting(backend, 'LOGIN_ERROR_URL', LOGIN_ERROR_URL)
    if msg:
        messages.error(request, msg)

    if redirect_value and redirect_value != url:
        #redirect_value = quote(redirect_value)
        if '?' in url:
            url += '&%s=%s' % (REDIRECT_FIELD_NAME, redirect_value)
        else:
            url += '?%s=%s' % (REDIRECT_FIELD_NAME, redirect_value)
    return HttpResponseRedirect(url)



def social_complete(request, backend, *args, **kwargs):
    print 'social_complete social_complete social_complete social_complete'

    resp = complete(request, backend, *args, **kwargs)


    app_id = request.session.get('social_new_app_id')
    print type(resp), app_id, resp

    if type(resp) == HttpResponseRedirect and app_id:

        request.session.delete('social_new_app_id')
        token = get_connect_token(app_id, request.user.id, raw=True)

        redirect_to = str(resp['Location'])
        redirect_to = redirect_to\
            .replace('[user.id]', str(request.user.id)).replace('%5Buser.id%5D', str(request.user.id))\
            .replace('[new-token]', token).replace('%5Bnew-token%5D', token)

        resp = HttpResponseRedirect(redirect_to)


    return resp

# =========================================================
# People (public pages)
# =========================================================



def account_detail(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        return redirect('account_login')

    return people_detail(request, user.username)

def people_detail(request, username, people_id=None):

    # For user type name from url
    people = get_object_or_404(User, username=username)

    if not people_id:
        return redirect('people_detail', username, people.id)
    people = get_object_or_404(User, id=people_id)

    params_query = people.skills.replace(',', '+')
    params_query = params_query.replace(' ', '')
    interests = people.interests.all()
    for interest in interests:
        params_query += '+' + interest.title

    return render(request, 'account/detail.html', {
        'username': username,
        'people_id': people_id,
        'params_query': params_query,
        'instance': people
    })


def people_list(request):
    if settings.LIST_PAGE_REDIRECT != 'organization_role_list':
        return redirect(settings.LIST_PAGE_REDIRECT, 'people')

    return render(request, 'party/list.html', {
        'party_list_title': 'People',
        'tab_list_config': json.dumps(TAB_LIST_CONFIG),
        'promote_list_config': json.dumps(PROMOTE_LIST_CONFIG)
    })

def people_role_list(request, user_role_permalink):
    return render(request, 'party/list.html', {
        'party_list_title': 'People',
        'tab_list_config': json.dumps(TAB_LIST_ROLE_CONFIG[user_role_permalink]),
        'promote_list_config': json.dumps(PROMOTE_LIST_ROLE_CONFIG[user_role_permalink]),
        'role_permalink': user_role_permalink,
    })

def people_role_detail(request, username, people_id=None):

    # For user type name from url
    people = get_object_or_404(User, username=username)
    if not people_id:
        return redirect('people_detail', username, people.id)
    people = get_object_or_404(User, id=people_id)

    params_query = people.skills.replace(',', '+')
    params_query = params_query.replace(' ', '')
    interests = people.interests.all()
    for interest in interests:
        params_query += '+' + interest.title

    return render(request, 'account/detail.html', {
        'username': username,
        'people_id': people_id,
        'params_query': params_query,
        'instance': people
    })


@login_required
def account_app(request):
    return render(request, 'account/app.html', {'apps': AppConnect.objects.filter(created_by=request.user)})

#@login_required
def account_app_detail(request, pk=None):

    model_class = AppConnect
    instance = get_object_or_404(model_class, app_id=pk)
    context = {'instance': instance}

    return render(request, 'account/app_detail.html', context)


@login_required
def account_app_form(request, pk=None):
    model_class = AppConnect
    form_class = AppConnectForm

    if pk:
        instance = get_object_or_404(model_class, app_id=pk)

    else:
        instance = model_class()

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():

            instance = form.save(commit=False)

            if not pk:
                instance.app_id = uuid.uuid1().int>>64

            try:
                instance_files = instance._meta.get_field('image')
                if instance_files:
                    instance_files.save_form_data(instance, form.cleaned_data['image'])
            except FieldDoesNotExist:
                pass

            instance.created_by = request.user

            instance.save()

            message_success = get_success_message(instance, not bool(pk))
            messages.success(request, message_success)


            return redirect('account_app_edit', instance.app_id)

    else:
        form = form_class(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'account/app_form.html', context)


def safe_app_redirect(app, redirect_uri):

    try:
        if type(long(app)) == long:
            try:

                app = AppConnect.objects.get(app_id=app)

            except AppConnect.DoesNotExist:
                return False, []

    except (ValueError, TypeError):
        pass

    o = urlparse(redirect_uri)

    allow_hosts = [app.site_uri, '127.0.0.1', '0.0.0.0', 'localhost', 'local']
    if not o.hostname in allow_hosts:
        return False, allow_hosts

    return True, app, allow_hosts


def account_connect(request):

    new_app_id = request.GET.get('new_app_id')


    try:
        app = AppConnect.objects.get(app_id=new_app_id)
    except AppConnect.DoesNotExist:
        return render(request, 'account/app_connect_error.html', {'message': 'App id <em>%s</em> does not exist' % new_app_id})

    redirect_uri = request.GET.get('redirect_uri') or ('//:%s' % app.site_uri)
    o = urlparse(redirect_uri)

    is_safe, app, allow_hosts = safe_app_redirect(app, redirect_uri)
    if not is_safe:
        return render(request, 'account/app_connect_error.html', {
            'message': 'The redirect uri <em>%s</em> does not allow, list of collected redirect uri below<br> %s' % (redirect_uri, ', '.join(allow_hosts))
        })

    redirect_to = '%s?new_app_id=%s&next=%s' % (reverse('account_login'), app.app_id, urllib.quote_plus(redirect_uri))
    return redirect(redirect_to)


def account_your_receive_new_token_path(request):
    token = request.GET.get('new_token')
    return render(request, 'account/app_your_receive_new_token_path.html', {'token': token})


def account_app_post_message(request, token=None):
    raw_token, app_id, user_id = token.split('--')
    if token == get_connect_token(app_id, user_id):
        res = UserResource()
        request_bundle = res.build_bundle(request=request)
        user = res.obj_get(request_bundle, id=user_id)
        user_bundle = res.build_bundle(request=request, obj=user)
        user_json = res.serialize(None, res.full_dehydrate(user_bundle), "application/json")

        return render(request, 'account/app_post_message.html', {'data': user_json})


    return render(request, 'account/app_connect_error.html', {
        'message': 'Your request token <em>%s</em> miss match' % token
    })


def account_connect_js(request):
    return render(request, 'account/app-connect.js', content_type='application/javascript')









