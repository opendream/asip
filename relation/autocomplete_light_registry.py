import autocomplete_light
from django.db.models import QuerySet
from account.functions import user_render_reference

from account.models import User
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

    choices = Organization.objects.filter().order_by('name')
    search_fields = ['name', 'summary']

    display_edit_link = False
    field_name = 'adds'

    # def choices_for_request(self):
    #     print 'choices_for_request xxxx'
    #     print self.request
    #     return super(OrganizationAutocomplete, self).choices_for_request()

    def choice_label(self, choice):

        return organization_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))
autocomplete_light.register(Organization, OrganizationAutocomplete)


class PartyAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = Party.objects.filter().order_by('organization__name', 'user__first_name', 'user__last_name')
    search_fields = ['organization__name', 'organization__summary', 'user__email', 'user__username', 'user__first_name', 'user__last_name']

    display_edit_link = False
    field_name = None

    def choice_label(self, choice):
        return party_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))
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


class OrganizationPartnerAutocomplete(OrganizationAutocomplete):
    field_name = 'partners'
autocomplete_light.register(Organization, OrganizationPartnerAutocomplete)


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