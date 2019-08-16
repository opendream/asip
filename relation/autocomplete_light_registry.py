import autocomplete_light
import six
from django.db.models import QuerySet
from account.functions import user_render_reference

from account.models import User
from common.constants import STATUS_PUBLISHED, STATUS_PENDING, TYPE_PROGRAM, TYPE_STARTUP, TYPE_SUPPORTING_ORGANIZATION
from organization.functions import organization_render_reference
from organization.models import Organization
from party.functions import party_render_reference
from party.models import Party
from relation.functions import experience_render_reference, received_funding_render_reference
from relation.models import UserExperienceOrganization, PartyReceivedFundingParty, PartyReceivedInvestingParty, \
    CmsHasParty


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = User.objects.filter().order_by('first_name', 'last_name')

    search_fields = ['email', 'username', 'first_name', 'last_name']

    display_edit_link = False
    field_name = 'adds'

    def choice_label(self, choice):

        return user_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))
autocomplete_light.register(User, UserAutocomplete)


class OrganizationAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = Organization.objects.filter(status__in=[STATUS_PUBLISHED, STATUS_PENDING]).extra(select={'is_published': 'status = %d' % STATUS_PUBLISHED, 'is_pending': 'status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending', '-status', 'name')
    backward_choices = Organization.objects.filter().extra(select={'is_published': 'status = %d' % STATUS_PUBLISHED, 'is_pending': 'status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending', '-status', 'name')

    search_fields = ['name', 'summary']

    display_edit_link = False
    field_name = 'adds'
    src_field_name = ''
    dst_field_name = ''

    def choice_label(self, choice):

        instance = None
        try:
            instance = self.instance
        except:
            pass

        return organization_render_reference(choice, self.display_edit_link, self.field_name, instance, self.src_field_name, self.dst_field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))

    def choices_for_values(self):
        """
        Return ordered choices which pk are in
        :py:attr:`~.base.AutocompleteInterface.values`.
        """
        assert self.choices is not None, 'choices should be a queryset'

        # choices = self.choices.filter(pk__in=self.values)
        # if not choices.exists():
        choices = self.backward_choices.filter(pk__in=self.values)

        return self.order_choices(choices)

    def choices_for_request(self):
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'

        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude')

        conditions = self._choices_for_request_conditions(q,
                self.search_fields)

        out = self.order_choices(self.choices.filter(conditions).exclude(pk__in=exclude))

        if not out.exists():
            out = self.order_choices(self.backward_choices.filter(conditions).exclude(pk__in=exclude))

        return out[0:self.limit_choices]

autocomplete_light.register(Organization, OrganizationAutocomplete)

class PartyAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = Party.objects.filter(organization__isnull=False, organization__status__in=[STATUS_PUBLISHED, STATUS_PENDING]).exclude(organization__type_of_organization=TYPE_PROGRAM).extra(select={'is_published': 'organization_organization.status = %d' % STATUS_PUBLISHED, 'is_pending': 'organization_organization.status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending', 'organization__name', 'user__first_name', 'user__last_name')
    backward_choices = Party.objects.filter(organization__isnull=False).exclude(organization__type_of_organization=TYPE_PROGRAM).extra(select={'is_published': 'organization_organization.status = %d' % STATUS_PUBLISHED, 'is_pending': 'organization_organization.status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending', 'organization__name', 'user__first_name', 'user__last_name')

    search_fields = ['organization__name', 'organization__summary', 'user__email', 'user__username', 'user__first_name', 'user__last_name']

    display_edit_link = False
    field_name = None

    def choice_label(self, choice):
        return party_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))
    
    def choices_for_values(self):
        """
        Return ordered choices which pk are in
        :py:attr:`~.base.AutocompleteInterface.values`.
        """
        assert self.choices is not None, 'choices should be a queryset'

        choices = self.choices.filter(pk__in=self.values)
        if not choices.exists():
            choices = self.backward_choices.filter(pk__in=self.values)
        return self.order_choices(choices)

    def choices_for_request(self):
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude')

        conditions = self._choices_for_request_conditions(q,
                self.search_fields)

        out = self.order_choices(self.choices.filter(conditions).exclude(pk__in=exclude))

        if not out.exists():
            out = self.order_choices(self.backward_choices.filter(conditions).exclude(pk__in=exclude))

        return out[0:self.limit_choices]

autocomplete_light.register(Organization, PartyAutocomplete)


class UserAdminAutocomplete(UserAutocomplete):
    field_name = 'admins'
autocomplete_light.register(User, UserAdminAutocomplete)

class UserReceiverAutocomplete(UserAutocomplete):
    field_name = 'receivers'
autocomplete_light.register(User, UserReceiverAutocomplete)

class UserPeopleAutocomplete(UserAutocomplete):
    field_name = 'peoples'

    choices = User.objects.order_by('-organization_has_people_dst__priority', '-id').distinct()
autocomplete_light.register(User, UserPeopleAutocomplete)


class OrganizationStartupAutocomplete(OrganizationAutocomplete):
    choices = OrganizationAutocomplete.choices.filter(type_of_organization=TYPE_STARTUP)
    backward_choices = OrganizationAutocomplete.backward_choices.filter(type_of_organization=TYPE_STARTUP)
autocomplete_light.register(Organization, OrganizationStartupAutocomplete)

class OrganizationPartnerAutocomplete(OrganizationAutocomplete):
    field_name = 'partners'
    src_field_name = 'partner_src'
    dst_field_name = 'partner_dst'

autocomplete_light.register(Organization, OrganizationPartnerAutocomplete)


class OrganizationGovernmentPartnerAutocomplete(OrganizationAutocomplete):
    field_name = 'partners'
    src_field_name = 'partner_src'
    dst_field_name = 'partner_dst'

    choices = OrganizationAutocomplete.choices.filter(type_of_organization=TYPE_SUPPORTING_ORGANIZATION, organization_types__permalink='government')
    backward_choices = OrganizationAutocomplete.backward_choices.filter(type_of_organization=TYPE_SUPPORTING_ORGANIZATION, organization_types__permalink='government')

autocomplete_light.register(Organization, OrganizationGovernmentPartnerAutocomplete)

class OrganizationMediaPartnerAutocomplete(OrganizationAutocomplete):
    field_name = 'partners'
    src_field_name = 'partner_src'
    dst_field_name = 'partner_dst'

    choices = OrganizationAutocomplete.choices.filter(type_of_organization=TYPE_SUPPORTING_ORGANIZATION, organization_types__permalink='media')
    backward_choices = OrganizationAutocomplete.backward_choices.filter(type_of_organization=TYPE_SUPPORTING_ORGANIZATION, organization_types__permalink='media')

autocomplete_light.register(Organization, OrganizationMediaPartnerAutocomplete)

class OrganizationAssociationPartnerAutocomplete(OrganizationAutocomplete):
    field_name = 'partners'
    src_field_name = 'partner_src'
    dst_field_name = 'partner_dst'

    choices = OrganizationAutocomplete.choices.filter(type_of_organization=TYPE_SUPPORTING_ORGANIZATION, organization_types__permalink='association')
    backward_choices = OrganizationAutocomplete.backward_choices.filter(type_of_organization=TYPE_SUPPORTING_ORGANIZATION, organization_types__permalink='association')

autocomplete_light.register(Organization, OrganizationAssociationPartnerAutocomplete)

class PartySupporterAutocomplete(PartyAutocomplete):
    field_name = 'supporters'
autocomplete_light.register(Party, PartySupporterAutocomplete)


class PartyInvestorAutocomplete(PartyAutocomplete):
    field_name = 'investors'
autocomplete_light.register(Party, PartyInvestorAutocomplete)


class OrganizationRecipientAutocomplete(OrganizationAutocomplete):
    field_name = 'recipients'
autocomplete_light.register(Organization, OrganizationRecipientAutocomplete)


class OrganizationInvestRecipientAutocomplete(OrganizationAutocomplete):
    field_name = 'recipients'
autocomplete_light.register(Organization, OrganizationInvestRecipientAutocomplete)


class OrganizationExperienceAutocomplete(OrganizationAutocomplete):
    field_name = 'dst'
autocomplete_light.register(Organization, OrganizationExperienceAutocomplete)

class UserExperienceOrganizationAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = UserExperienceOrganization.objects.filter().order_by('-ordering')
    search_fields = ['title']

    display_edit_link = True
    field_name = 'experiences'

    def choice_label(self, choice):

        return experience_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))
autocomplete_light.register(UserExperienceOrganization, UserExperienceOrganizationAutocomplete)



# Funding

class PartyReceivedFundingAutocomplete(PartyAutocomplete):
    field_name = 'dst'
autocomplete_light.register(Party, PartyReceivedFundingAutocomplete)

class PartyReceivedFundingPartyAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = PartyReceivedFundingParty.objects.filter().order_by('ordering')
    search_fields = ['title']

    display_edit_link = True
    field_name = 'received_fundings'

    def choice_label(self, choice):

        return received_funding_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))
autocomplete_light.register(PartyReceivedFundingParty, PartyReceivedFundingPartyAutocomplete)


class PartyGivedFundingAutocomplete(PartyAutocomplete):
    field_name = 'src'
autocomplete_light.register(Party, PartyGivedFundingAutocomplete)

class PartyGivedFundingPartyAutocomplete(PartyReceivedFundingPartyAutocomplete):
    field_name = 'gived_fundings'
autocomplete_light.register(PartyReceivedFundingParty, PartyGivedFundingPartyAutocomplete)


# Investing

class PartyReceivedInvestingAutocomplete(PartyAutocomplete):
    field_name = 'dst'
autocomplete_light.register(Party, PartyReceivedInvestingAutocomplete)

class PartyReceivedInvestingPartyAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = PartyReceivedInvestingParty.objects.filter().order_by('ordering')
    search_fields = ['title']

    display_edit_link = True
    field_name = 'received_investings'

    def choice_label(self, choice):

        return received_funding_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))
autocomplete_light.register(PartyReceivedFundingParty, PartyReceivedInvestingPartyAutocomplete)


class PartyGivedInvestingAutocomplete(PartyAutocomplete):
    field_name = 'src'
autocomplete_light.register(Party, PartyGivedInvestingAutocomplete)

class PartyGivedInvestingPartyAutocomplete(PartyReceivedInvestingPartyAutocomplete):
    field_name = 'gived_investings'
autocomplete_light.register(PartyReceivedInvestingParty, PartyGivedInvestingPartyAutocomplete)

class CmsHasPartyAutocomplete(PartyAutocomplete):
    field_name = 'in_the_news'
autocomplete_light.register(CmsHasParty, CmsHasPartyAutocomplete)