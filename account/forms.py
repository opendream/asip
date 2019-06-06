from uuid import uuid1
import autocomplete_light
from django.conf import settings
from psycopg2._psycopg import DataError
from account.models import AppConnect
from account.pipeline import rewrite_username
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User   # fill in custom user info then save it
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from common.constants import SUMMARY_MAX_LENGTH
import files_widget
from common.forms import PermalinkForm, CommonModelForm
from organization.models import Organization
from party.autocomplete_light_registry import PortfolioAutocomplete
from party.models import Portfolio, Party
from relation.autocomplete_light_registry import UserExperienceOrganizationAutocomplete, \
    OrganizationRecipientAutocomplete, PartyGivedFundingPartyAutocomplete, PartyGivedInvestingPartyAutocomplete, \
    OrganizationInvestRecipientAutocomplete, OrganizationAutocomplete
from relation.models import UserExperienceOrganization, PartyReceivedFundingParty, PartyReceivedInvestingParty
from taxonomy.models import Country, UserRole, Topic
from tagging.forms import TagField
from tagging_autocomplete_tagit.widgets import TagAutocompleteTagIt


class EmailAuthenticationForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    remember_me = forms.NullBooleanField()

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')


        if email and password:
            self.user_cache = authenticate(username=email, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(_('Please, enter correct email/username and password.'))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account not activated.'))

        return self.cleaned_data


    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache




class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=80)

    check_is_active = True

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None, extra_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        params = {'email__iexact': email}
        if self.check_is_active:
            params['is_active'] = True

        active_users = UserModel._default_manager.filter(**params)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable

            if not user.has_usable_password():
                #continue
                pass
                
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'site_slogan': settings.SITE_SLOGAN,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'next': request.GET.get('next') or request.POST.get('next'),
                'query': request.GET or request.POST,
                'protocol': 'https' if use_https else 'http',
            }
            if extra_context:
                c.update(extra_context)
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name, c)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email], html_message=html_email)


class ResetPasswordForm(PasswordResetForm):

    check_is_active = False

    def clean_email(self):

        email = self.cleaned_data.get('email')

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise forms.ValidationError(_('Your email address is not registered.'))

        if not user.is_active:
            #raise forms.ValidationError(_('Your email address is not activated.'))
            pass

        return email


class InviteForm(PasswordResetForm):

    first_name  = forms.CharField(required=False, max_length=255, widget=forms.TextInput())
    last_name   = forms.CharField(required=False, max_length=255, widget=forms.TextInput())
    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())
    summary   = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    check_is_active = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        UserModel = get_user_model()
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is already in use.'))

        return email

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if str(image) == 'None':
            return None
        return image

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None, extra_context=None):

        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        image = self.cleaned_data.get('image')
        summary = self.cleaned_data.get('summary')

        UserModel = get_user_model()

        try:
            UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            password = str(uuid1())[0: 10].replace('-', '')

            username = rewrite_username(email)

            if len(username) > 30:
                raise forms.ValidationError(
                    _('Ensure this email prefix(characters before @) has at most 30 characters '))

            user = UserModel.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                summary=summary,
                is_active=False
            )
            if image:
                user.image = image

            user.set_password(password)
            user.save()

        super(InviteForm, self).save(
            domain_override,
            subject_template_name,
            email_template_name,
            use_https,
            token_generator,
            from_email,
            request,
            html_email_template_name,
            extra_context=extra_context
        )


class AccountEditForm(PermalinkForm):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())

    username    = forms.CharField(max_length=30)
    email       = forms.EmailField(max_length=75)
    gender      = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_gender'}), choices=GENDER_CHOICES)
    password    = forms.CharField(required=False, max_length=128, widget=forms.PasswordInput())
    password2   = forms.CharField(required=False, max_length=128, widget=forms.PasswordInput())
    first_name  = forms.CharField(required=True, max_length=30, widget=forms.TextInput())
    last_name   = forms.CharField(required=True, max_length=30, widget=forms.TextInput())
    skills = TagField(required=False, widget=TagAutocompleteTagIt(max_tags=False), help_text='')


    occupation  = forms.CharField(required=False, max_length=128, widget=forms.TextInput())
    summary = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':2, 'maxlength': SUMMARY_MAX_LENGTH}))
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    homepage_url = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    # Notification
    #   User relation
    notification_allow_email_send_organizationhaspeople = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organizationhaspeople'}))
    notification_allow_email_send_partysupportparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_partysupportparty'}))
    notification_allow_email_send_partyfollowparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_partyfollowparty'}))
    notification_allow_email_send_partycontactparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_partycontactparty'}))
    notification_allow_email_send_partytestifyparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_partytestifyparty'}))
    notification_allow_email_send_partyinvitetestifyparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_partyinvitetestifyparty'}))
    notification_allow_email_send_partylove = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_partylove'}))

    #   Organization relation

    notification_allow_email_send_organization_partypartnerparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_partypartnerparty'}))
    notification_allow_email_send_organization_userexperienceorganization = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_userexperienceorganization'}))
    notification_allow_email_send_organization_partysupportparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_partysupportparty'}))
    notification_allow_email_send_organization_partyfollowparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_partyfollowparty'}))
    notification_allow_email_send_organization_partycontactparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_partycontactparty'}))
    notification_allow_email_send_organization_partytestifyparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_partytestifyparty'}))
    notification_allow_email_send_organization_partyinvitetestifyparty = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_partyinvitetestifyparty'}))
    notification_allow_email_send_organization_partylove = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_organization_partylove'}))

    # Follower
    notification_allow_email_send_from_follow = forms.NullBooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': 'notification_allow_email_send_from_follow'}))
    # Taxonomy
    user_roles = forms.ModelMultipleChoiceField(required=True, queryset=UserRole.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_user_roles'}))
    interests = forms.ModelMultipleChoiceField(required=False, queryset=Topic.objects.all().filter(parent=None).order_by('title'), widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_interests'}))
    country = forms.ModelChoiceField(required=False, queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    # External
    facebook_url = forms.URLField(required=False, max_length=255, widget=forms.TextInput())
    twitter_url = forms.URLField(required=False, max_length=255, widget=forms.TextInput())
    linkedin_url = forms.URLField(required=False, max_length=255, widget=forms.TextInput())
    homepage_url = forms.URLField(required=False, max_length=255, widget=forms.TextInput())

    # SYSTEM
    promote = forms.NullBooleanField(widget=forms.CheckboxInput())

    organizations = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationAutocomplete,
            attrs={'placeholder': _('Type for search organization by name.'), 'class': 'form-control'}
        )
    )

    portfolios = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Portfolio.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PortfolioAutocomplete,
            attrs={'placeholder': _('Type for search portfolios by title'), 'class': 'form-control'}
        )
    )

    experiences = forms.ModelMultipleChoiceField(
        required=False,
        queryset=UserExperienceOrganization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(UserExperienceOrganizationAutocomplete)
    )

    recipients = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationRecipientAutocomplete,
            attrs={'placeholder': _('Type to search organizations by name.'), 'class': 'form-control'}
        )
    )
    gived_fundings = forms.ModelMultipleChoiceField(
        required=False,
        queryset=PartyReceivedFundingParty.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartyGivedFundingPartyAutocomplete)
    )

    invest_recipients = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Party.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationInvestRecipientAutocomplete,
            attrs={'placeholder': _('Type to search organizations or people by name.'), 'class': 'form-control'}
        )
    )
    gived_investings = forms.ModelMultipleChoiceField(
        required=False,
        queryset=PartyReceivedInvestingParty.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartyGivedInvestingPartyAutocomplete)
    )

    PERMALINK_FIELDS = ['username', 'email']

    def __init__(self, inst=None, model=None, request_user=None, required_password=False, *args, **kwargs):
        super(AccountEditForm, self).__init__(inst, model, request_user, *args, **kwargs)

        self.inst = inst

        if required_password:
            self.fields['password'].required = True
            self.fields['password2'].required = True

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(_('Password mismatch.'))
        return password2

    def clean_organizations(self):
        organizations = self.cleaned_data.get('organizations')
        user_roles = self.cleaned_data.get('user_roles')

        if user_roles and not user_roles.filter(permalink='individual') and not organizations:
            raise forms.ValidationError(_('This field is required.'))

        return organizations


class AccountRegisterForm(PasswordResetForm):

    check_is_active = False

    def clean_email(self):


        email = self.cleaned_data.get('email')
        UserModel = get_user_model()

        try:
            UserModel.objects.get(email=email, is_active=True)
            raise forms.ValidationError(_('This email is already in use.'))
        except UserModel.DoesNotExist:

            password = str(uuid1())[0: 10].replace('-', '')

            try:
                UserModel.objects.get(email=email)

            except UserModel.DoesNotExist:

                username = rewrite_username(email)

                if len(username) > 30:
                    raise forms.ValidationError(_('Ensure this email prefix(characters before @) has at most 30 characters '))

                user = UserModel.objects.create(username=username, email=email, is_active=False)
                user.set_password(password)
                user.save()


        return email


class AppConnectForm(CommonModelForm):


    class Meta:
        model = AppConnect
        exclude = ['created_by', 'is_deleted']

    def __init__(self, *args, **kwargs):
        super(AppConnectForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['app_id'].widget.attrs['readonly'] = True
        else:
            del(self.fields['app_id'])