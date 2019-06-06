# -*- coding: utf-8 -*-

import autocomplete_light
from django import forms
from django.conf import settings
from django.db.models import BLANK_CHOICE_DASH, Q

from django.utils.translation import ugettext_lazy as _

from ckeditor.widgets import CKEditorWidget
from mptt.forms import TreeNodeMultipleChoiceField
from common.functions import generate_year_range
from organization.autocomplete_light_registry import JobAutocomplete
from party.autocomplete_light_registry import PortfolioAutocomplete
from relation.autocomplete_light_registry import *
from common.constants import STATUS_CHOICES, SUMMARY_MAX_LENGTH, STATUS_PUBLISHED, STATUS_PENDING

from common.forms import PermalinkForm, CommonForm, CommonModelForm, PrettyRadioSelect, PrettyCheckboxSelectMultiple, BetterSelectDateWidget, \
    BetterDecimalField
from party.models import Party, Portfolio
from relation.models import PartyReceivedFundingParty
from tagging.forms import TagField
from special.models import Special
from tagging_autocomplete_tagit.widgets import TagAutocompleteTagIt
from taxonomy.models import TypeOfNeed, Topic, TypeOfSupport, Country, OrganizationRole, OrganizationType, \
    OrganizationProductLaunch, OrganizationFunding, OrganizationGrowthStage, InvestorType
from organization.models import Organization, AbstractOrganizationSection1, AbstractOrganizationSection2, \
                                AbstractOrganizationSection3, AbstractOrganizationSection4, AbstractOrganizationSection5, \
    Job
from account.models import User
import files_widget


# Formset
class TeamInformationForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first', 'placeholder': _('Name')}))
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control last', 'placeholder': _('Title')}))

class PhoneNumberOfOrganizationsHeadquartersForm(forms.Form):
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Phone Number')}))

class LocationOfOrganizationsOperatingFacilitiesForm(forms.Form):
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control first last', 'placeholder': _('Address'), 'rows': 2}))

class MeasurementYearValuesForm(forms.Form):
    year_of_datapoint = forms.CharField(required=True, widget=forms.Select(choices=generate_year_range(choices=True, empty_label='Year of Datapoint'), attrs={'class': 'form-control first last', 'placeholder': _('Year of datapoint')}))
    value_of_impact_1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Value of impact 1')}))
    value_of_impact_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Value of impact 2')}))
    value_of_impact_3 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Value of impact 3')}))

class Top3MajorInvestorsYearAndAmountForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control last', 'placeholder': _('Investor name, years, amounts')}))

class Top3MajorDonorsYearAndAmountForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control last', 'placeholder': _('Donor name, years, amounts')}))


exclude = [
    'store_phone_number_of_organizations_headquarters',
    'store_location_of_organizations_operating_facilities',
    'store_measurement_year_values',
    'store_top_3_major_investors_year_and_amount',
    'store_top_3_major_donors_year_and_amount',
    'store_team_information',
]

# Section 1
class OrganizationSection1EditForm(CommonModelForm):

    sector_activities = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.filter(level=0),
        required=False,
        widget=PrettyCheckboxSelectMultiple
    )

    class Meta:
        model = AbstractOrganizationSection1
        exclude = exclude
        widgets = {
            'report_start_date': BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day')),
            'report_end_date': BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day')),
            'year_founded': forms.Select(choices=generate_year_range(choices=True)),
            'gender_of_representative': PrettyRadioSelect(),
            'target_beneficiary': PrettyCheckboxSelectMultiple(),
        }





# Section 2
class OrganizationSection2EditForm(CommonModelForm):

    productservice_type = TreeNodeMultipleChoiceField(required=False, queryset=Topic.objects.all(), level_indicator=u'⌞',
                                         widget=PrettyCheckboxSelectMultiple())

    class Meta:
        model = AbstractOrganizationSection2
        exclude = exclude
        widgets = {
            'client_type': PrettyCheckboxSelectMultiple(),
            'client_locations': PrettyCheckboxSelectMultiple(),
        }


# Section 3
class OrganizationSection3EditForm(CommonModelForm):
    class Meta:
        model = AbstractOrganizationSection3
        exclude = exclude
        widgets = {
            'financial_statement_review': forms.CheckboxInput(),
        }


# Section 4
class OrganizationSection4EditForm(CommonModelForm):
    class Meta:
        model = AbstractOrganizationSection4
        exclude = exclude
        widgets = {}


# Section 5
class OrganizationSection5EditForm(CommonModelForm):
    class Meta:
        model = AbstractOrganizationSection5
        exclude = exclude

        POSSIBLE_FORM_OF_FINANCIAL_SUPPORT_CHOICES = (
            ('1', 'Grant'),
            ('2', 'Loan'),
            ('3', 'Equity')
        )

        widgets = {
            'possible_form_of_financial_support': PrettyCheckboxSelectMultiple(),
            'potential_use_of_investment': PrettyCheckboxSelectMultiple(),
            'possible_form_of_non_financial_support': PrettyCheckboxSelectMultiple()
        }


class OrganizationEditForm(PermalinkForm):

    permalink = forms.CharField()

    kind = forms.ChoiceField(
        label=_('What kind of your created ?'),
        required=True,
        widget=forms.RadioSelect(attrs={'id': 'id_kind'}),
        choices=Organization.KIND_CHOICES,
    )

    admins = forms.ModelMultipleChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(UserAdminAutocomplete,
            attrs={'placeholder': _('Type to search people by name.'), 'class': 'form-control'}
        )
    )

    peoples = forms.ModelMultipleChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(UserPeopleAutocomplete,
            attrs={'placeholder': _('Type for search people by name.'), 'class': 'form-control'}
        )
    )
    partners = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationPartnerAutocomplete,
            attrs={'placeholder': _('Type to search organizations by name.'), 'class': 'form-control'}
        )
    )
    supporters = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Party.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartySupporterAutocomplete,
            attrs={'placeholder': _('Type to search organizations or people by name.'), 'class': 'form-control'}
        )
    )
    recipients = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationRecipientAutocomplete,
            attrs={'placeholder': _('Type to search organizations by name.'), 'class': 'form-control'}
        )
    )
    investors = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Party.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartyInvestorAutocomplete,
            attrs={'placeholder': _('Type to search organizations or people by name.'), 'class': 'form-control'}
        )
    )
    invest_recipients = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Party.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationInvestRecipientAutocomplete,
            attrs={'placeholder': _('Type to search organizations or people by name.'), 'class': 'form-control'}
        )
    )

    portfolios = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Portfolio.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PortfolioAutocomplete,
            attrs={'placeholder': _('Type for search portfolios by title.'), 'class': 'form-control'}
        )
    )

    jobs = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Job.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(JobAutocomplete,
                                                       attrs={
                                                           'placeholder': _('Type to search jobs by title.'),
                                                            'class': 'form-control'
                                                       }
        )
    )

    received_fundings = forms.ModelMultipleChoiceField(
        required=False,
        queryset=PartyReceivedFundingParty.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartyReceivedFundingPartyAutocomplete)
    )

    gived_fundings = forms.ModelMultipleChoiceField(
        required=False,
        queryset=PartyReceivedFundingParty.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartyGivedFundingPartyAutocomplete)
    )

    received_investings = forms.ModelMultipleChoiceField(
        required=False,
        queryset=PartyReceivedInvestingParty.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartyReceivedInvestingPartyAutocomplete)
    )

    gived_investings = forms.ModelMultipleChoiceField(
        required=False,
        queryset=PartyReceivedInvestingParty.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(PartyGivedInvestingPartyAutocomplete)
    )

    # Internal
    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())
    images = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImagesWidget())

    name = forms.CharField(max_length=255, widget=forms.TextInput())
    summary = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'maxlength': SUMMARY_MAX_LENGTH}))
    description = forms.CharField(required=True, widget=CKEditorWidget())

    # Taxonomy
    type_of_needs = forms.ModelMultipleChoiceField(required=False, queryset=TypeOfNeed.objects.all(),
                                                   widget=forms.CheckboxSelectMultiple(
                                                       attrs={'id': 'id_type_of_needs'}))
    type_of_supports = forms.ModelMultipleChoiceField(required=False, queryset=TypeOfSupport.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple(
                                                      attrs={'id': 'id_type_of_supports'}))

    organization_primary_role = forms.ModelChoiceField(required=True, queryset=OrganizationRole.objects.all(),
                                                        widget=forms.RadioSelect(
                                                            attrs={'id': 'id_organization_primary_role'}))
    organization_roles = forms.ModelMultipleChoiceField(required=True, queryset=OrganizationRole.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple(
                                                          attrs={'id': 'id_organization_roles'}))

    organization_types = forms.ModelMultipleChoiceField(required=False, queryset=OrganizationType.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple(
                                                            attrs={'id': 'id_organization_types'}))
    investor_types = forms.ModelMultipleChoiceField(required=False, queryset=InvestorType.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple(
                                                            attrs={'id': 'id_investor_types'}))

    topics = TreeNodeMultipleChoiceField(queryset=Topic.objects.all(), level_indicator=u'⌞', widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_topics'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    product_launch = forms.ModelChoiceField(required=False, queryset=OrganizationProductLaunch.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    funding = forms.ModelChoiceField(required=False, queryset=OrganizationFunding.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    request_funding = forms.ModelChoiceField(required=False, queryset=OrganizationFunding.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    deal_size_start = forms.IntegerField(required=False, min_value=0, max_value=100000000000, widget=forms.NumberInput)
    deal_size_end = forms.IntegerField(required=False, min_value=0, max_value=100000000000, widget=forms.NumberInput)

    # External
    facebook_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Facebook URL')}))
    twitter_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Twitter URL')}))
    linkedin_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Linkedin URL')}))
    homepage_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Homepage URL')}))

    # Meta
    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=STATUS_CHOICES)
    specials = forms.ModelMultipleChoiceField(required=False, queryset=Special.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_specials'}))

    def __init__(self, inst=None, model=None, request_user=None, *args, **kwargs):


        super(OrganizationEditForm, self).__init__(inst, model, request_user, *args, **kwargs)


        if inst.type_of_organization in [inst.TYPE_SOCIAL_ENTERPRISE, inst.TYPE_STARTUP]:
            self.fields['type_of_needs'].required = True

            self.fields['growth_stage'] = forms.ModelChoiceField(required=False, queryset=OrganizationGrowthStage.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))


            if inst.type_of_organization in [inst.TYPE_STARTUP]:
                self.fields['product_launch'].required = True
                self.fields['funding'].required = True

        elif inst.type_of_organization == inst.TYPE_SUPPORTING_ORGANIZATION:

            self.fields['growth_stage'] = forms.ModelMultipleChoiceField(
                required=False,
                queryset=OrganizationGrowthStage.objects.all(),
                widget=forms.CheckboxSelectMultiple(
                attrs={'id': 'id_growth_stage'})
            )


        # bypass check required
        if self.request_user and self.request_user.is_editor:
            for field_name, field in self.fields.iteritems():
                if hasattr(field, 'required'):
                    field.required = False

            self.fields['kind'].required = True
            self.fields['name'].required = True
            self.fields['permalink'].required = True

    def clean(self):

        cleaned_data = super(OrganizationEditForm, self).clean()

        # bypass check required
        if self.request_user and self.request_user.is_editor:
            return cleaned_data


        for role in cleaned_data['organization_roles'].all():

            field_name = '%s_types' % role.permalink

            if role.permalink == Organization.TYPE_SUPPORTING_ORGANIZATION:
                self.fields['organization_types'].required = True
                self.fields['type_of_supports'].required = True
                self.validate_required_field(cleaned_data, 'organization_types')
                self.validate_required_field(cleaned_data, 'type_of_supports')

            else:
                field = self.fields.get(field_name)
                if field:
                    field.required = True

                self.validate_required_field(cleaned_data, field_name)

        return cleaned_data


    def validate_required_field(self, cleaned_data, field_name, message="This field is required"):
        if (field_name in cleaned_data and (cleaned_data[field_name] is None or (hasattr(cleaned_data[field_name], 'all') and cleaned_data[field_name].all().count() == 0))):
            self._errors[field_name] = self.error_class([message])

            del cleaned_data[field_name]

class OrganizationEditInlineForm(CommonForm):
    type_of_organization = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'id': 'id_type_of_organization'}), choices=Organization.EXPAND_TYPE_CHOICES)

    name = forms.CharField(max_length=255, widget=forms.TextInput())
    image = files_widget.forms.FilesFormField(required=False, fields=(
        forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ),
                                              widget=files_widget.forms.widgets.ImageWidget())



class JobEditForm(CommonForm):


    def __init__(self, *args, **kwargs):
        try:
            user = kwargs.pop('user')
        except KeyError:
            user = None
        super(JobEditForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['organization'].queryset = Organization.objects.filter(Q(admins=user)|Q(created_by=user))


    title = forms.CharField(max_length=255, widget=forms.TextInput())
    contact_information = forms.CharField(widget=CKEditorWidget(config_name='minimal'))
    description = forms.CharField(required=False, widget=CKEditorWidget(config_name='default'))


    role = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'form-control'}), choices=Job.ROLE_CHOICES)

    position = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Job.POSITION_CHOICES)

    salary_min = forms.IntegerField(required=False, min_value=0, max_value=1000000000)
    salary_max = forms.IntegerField(required=False, min_value=0, max_value=1000000000)

    equity_min = forms.DecimalField(required=False, min_value=0, max_value=1000000000, max_digits=10, decimal_places=2)
    equity_max = forms.DecimalField(required=False, min_value=0, max_value=1000000000, max_digits=10, decimal_places=2)

    remote = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'id_remote'}), choices=Job.REMOTE_CHOICES)
    years_of_experience = forms.IntegerField(required=False)

    country = forms.ModelChoiceField(required=True, queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    skills = TagField(required=False, widget=TagAutocompleteTagIt(max_tags=False))


    status = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=Job.STATUS_CHOICES, initial=STATUS_PUBLISHED)

    organization = forms.ModelChoiceField(required=False, queryset=Organization.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))