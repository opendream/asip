# -*- coding: utf-8 -*-

import autocomplete_light
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import BLANK_CHOICE_DASH, Q
from django.forms import BaseFormSet

from django.utils.translation import ugettext_lazy as _
from djmoney.forms import MoneyField

from account.forms import InviteForm
from ckeditor.widgets import CKEditorWidget
from mptt.forms import TreeNodeMultipleChoiceField, TreeNodeChoiceField
from common.functions import generate_year_range, english_validator

from organization.autocomplete_light_registry import JobAutocomplete, ProgramAutocomplete, \
    StaffAutocomplete, ProgramInlineAutocomplete, InTheNewsAutocomplete

from party.autocomplete_light_registry import PortfolioAutocomplete
from common.constants import STATUS_CHOICES, SUMMARY_MAX_LENGTH, STATUS_PUBLISHED, STATUS_PENDING, \
    TYPE_PROGRAM, TYPE_STARTUP, TYPE_INVESTOR, STATUS_DRAFT, TYPE_SUPPORTING_ORGANIZATION

from common.forms import PermalinkForm, CommonForm, CommonModelForm, PrettyRadioSelect, PrettyCheckboxSelectMultiple, BetterSelectDateWidget, \
    BetterDecimalField, MultiCharField, RequiredNullBooleanField, EnglishCharField
from party.models import Party, Portfolio
from relation.autocomplete_light_registry import OrganizationStartupAutocomplete, UserAdminAutocomplete, UserPeopleAutocomplete, \
    OrganizationPartnerAutocomplete, PartySupporterAutocomplete, PartyInvestorAutocomplete, \
    OrganizationRecipientAutocomplete, OrganizationInvestRecipientAutocomplete, PartyReceivedFundingPartyAutocomplete, \
    PartyGivedFundingPartyAutocomplete, PartyReceivedInvestingPartyAutocomplete, PartyGivedInvestingPartyAutocomplete, \
    OrganizationGovernmentPartnerAutocomplete, OrganizationMediaPartnerAutocomplete, \
    OrganizationAssociationPartnerAutocomplete
from relation.models import PartyReceivedFundingParty, PartyReceivedInvestingParty
from tagging.forms import TagField
from special.models import Special
from tagging_autocomplete_tagit.widgets import TagAutocompleteTagIt
from taxonomy.models import TypeOfNeed, Topic, TypeOfSupport, Country, OrganizationRole, OrganizationType, \
    OrganizationProductLaunch, OrganizationFunding, OrganizationGrowthStage, InvestorType, TypeOfInvestmentStage, \
    TypeOfInvestment, TypeOfStageOfParticipant, TypeOfFocusIndustry, TypeOfFocusSector, ProgramType, TypeOfAttachment, \
    TypeOfFinancialSource, TypeOfAssistantship, TypeOfFunding, TypeOfOffice, JobRole, Location
from organization.models import Organization, AbstractOrganizationSection1, AbstractOrganizationSection2, \
    AbstractOrganizationSection3, AbstractOrganizationSection4, AbstractOrganizationSection5, \
    Job, Program, OrganizationStaff, AbstractOrganizationAttachment, InTheNews
from account.models import User
import files_widget



exclude = [
    'store_phone_number_of_organizations_headquarters',
    'store_location_of_organizations_operating_facilities',
    'store_measurement_year_values',
    'store_top_3_major_investors_year_and_amount',
    'store_top_3_major_donors_year_and_amount',
    'store_team_information',
]


class OrganizationRequiredForm(forms.Form):

    def __init__(self, inst=None, model=None, request_user=None, *args, **kwargs):
        try:
            super(OrganizationRequiredForm, self).__init__(inst, model, request_user, *args, **kwargs)
        except TypeError:
            super(OrganizationRequiredForm, self).__init__(*args, **kwargs)


        required_map = {
            TYPE_STARTUP: {
                'required_list': [
                    'name', 'permalink', 'company_registration_number', 'date_of_establishment',
                    'location_of_organizations_headquarters', 'store_email_of_organizations_headquarters', 'phone_number', 'office_type',
                    'focus_sector', 'stage_of_participants',
                    'description',
                    'name_of_representative', 'title_of_contact_person', 'email_of_contact_person', 'phone_number_of_contact_person',
                    'is_register_to_nia',
                ],
                'is_register_to_nia': [
                    {
                        'value': 'True',
                        'required_list': [
                            'company_vision', 'company_mission', 'business_model', 'growth_strategy',
                            'key_person',
                            'has_received_investment', 'financial_source',
                            # 'received_fundings', 
                            'has_taken_equity_in_startup',

                            'attachments_incorporation_registration_certificate',
                        ]
                    }
                ],
                'has_taken_equity_in_startup': [
                    {
                        'value': 'True',
                        'required_list': [
                            'taken_equity_amount',
                        ]
                    }
                ]
            },
            TYPE_INVESTOR: {
                'required_list': [
                    'name', 'permalink', 'investor_type',
                    'location_of_organizations_headquarters', 'store_email_of_organizations_headquarters', 'phone_number',
                    'focus_sector',
                    'description',
                    'name_of_representative', 'title_of_contact_person', 'email_of_contact_person', 'phone_number_of_contact_person',
                    'is_register_to_nia',
                ],
                'is_register_to_nia': [
                    {
                        'value': 'True',
                        'required_list': [
                            'money_deal_size_start', 'money_deal_size_end', 'specialty',
                            'funding_type',
                            'announced_date', 'closed_date',
                            'organization_funding_round',
                            'money_money_raise', 'money_target_funding', 'money_pre_money_valuation', 'is_lead_investor', 'has_taken_equity_in_fund_organization',

                            'attachments_incorporation_registration_certificate',
                            'attachments_financial_statement',
                            'attachments_investment_portfolio',
                        ]
                    }
                ],
                'investor_type': [
                    {
                        'value': '2',
                        'required_list': [
                            'gender', 'nationality', 'country_of_birth', 'date_of_birth', 'id_card', 'issued_at', 'date_of_issued_date', 'expired_date',
                        ],
                    },
                    {
                        'value': '3',
                        'required_list': [
                            'company_registration_number', 'date_of_establishment', 'number_of_employees',
                        ]
                    },
                    {
                        'value': '5',
                        'required_list': [
                            'company_registration_number', 'date_of_establishment', 'number_of_employees',
                        ]
                    }
                ],
                'is_lead_investor': [
                    {
                        'value': 'True',
                        'required_list': [
                            'money_amount_of_money_invested',
                        ]
                    }
                ]
            },
            TYPE_SUPPORTING_ORGANIZATION: {
                'required_list': [
                    'name', 'permalink', 'organization_types',
                    'location_of_organizations_headquarters', 'store_email_of_organizations_headquarters', 'phone_number',
                    'focus_sector',
                    'description',
                    'name_of_representative', 'title_of_contact_person', 'email_of_contact_person', 'phone_number_of_contact_person',
                ]
            },
            TYPE_PROGRAM: {
                'required_list': [
                    'name', 'permalink', 'program_type', 'date_of_establishment',
                    'organization',
                    'is_partner',
                    'focus_sector', 'focus_industry',
                    'description',
                    'name_of_representative', 'title_of_contact_person', 'email_of_contact_person', 'phone_number_of_contact_person',
                    'is_register_to_nia',
                ],
                'is_partner': [
                    {
                        'value': 'True',
                        'required_list': [
                            'partners',
                        ]
                    }
                ],
                'is_register_to_nia': [
                    {
                        'value': 'True',
                        'required_list': [
                            'mentor',
                            'staff',
                            'is_acting_as_an_investor',
                            'has_invited_in_participants_team',
                            'investment_stage_type', 'amount_total_stage',
                            'has_taken_equity_in_participating_team', 'does_provide_financial_supports',
                            # 'total_teams_applying', 'total_teams_accepted', 'total_participants_accepted', 'total_graduated_teams_accepted', 'total_training_program', 'total_organized_event', 'total_coached_staff', 'total_assisting_staff', 'total_approximated_products',
                            'period_of_engagement',
                            'does_provide_working_spaces', 'is_own_working_space', 'does_provide_service_and_facility',

                            'attachments_summary_of_the_activities_of_the_program',
                            'attachments_long_term_sustainable_revenue_model',
                            'attachments_resumes_or_portfolio_of_mentors_coaches_speaker_and_trainers',
                            'attachments_program_plans_in_the_future',
                            'attachments_list_of_notable_startup_team_alumni',
                            'attachments_list_of_organization_or_program_partners',
                        ]
                    }
                ],
                'has_invited_in_participants_team': [
                    {
                        'value': 'True',
                        'required_list': [
                            'investment_type',
                        ],
                    }
                ],
                'does_provide_financial_supports': [
                    {
                        'value': 'True',
                        'required_list': [
                            'amount_of_financial_supports',
                        ],
                    }
                ],
                'does_provide_working_spaces': [
                    {
                        'value': 'True',
                        'required_list': [
                            'address', 'tel', 'email',
                        ],
                    }
                ],
                'does_provide_service_and_facility': [
                    {
                        'value': 'True',
                        'required_list': [
                            'specify_service',
                        ],
                    }
                ],
            }
        }

        required_map_type = None

        if self.data.get('type_of_organization'):
            required_map_type = required_map.get(self.data.get('type_of_organization'))

        # bypass check required
        if (hasattr(self, 'request_user') and self.request_user and hasattr(self.request_user, 'is_editor') and self.request_user.is_editor) or (int(self.data.get('status', 0)) == STATUS_DRAFT):
            for field_name, field in self.fields.iteritems():
                if hasattr(field, 'required') and field_name not in ['name', 'permalink']:
                    field.required = False

        elif required_map_type:

            if required_map_type.get('required_list'):
                for field_name, field in self.fields.iteritems():
                    if hasattr(field, 'required'):
                        field.required = field_name in required_map_type.get('required_list')

            for depen_required_field, items in required_map_type.iteritems():

                if depen_required_field == 'required_list':
                    continue

                for obj in items:
                    if self.data.get(depen_required_field) != obj['value']:
                        continue

                    for field_name, field in self.fields.iteritems():
                        if hasattr(field, 'required') and field_name in obj['required_list']:
                            field.required = True


# Section 1
class OrganizationSection1EditForm(CommonModelForm, OrganizationRequiredForm):

    sector_activities = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.filter(level=0),
        required=False,
        widget=PrettyCheckboxSelectMultiple
    )

    location_of_organizations_headquarters = EnglishCharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control first last'}))

    title_of_contact_person = EnglishCharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    phone_number_of_contact_person = EnglishCharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

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
class OrganizationSection2EditForm(CommonModelForm, OrganizationRequiredForm):

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
class OrganizationSection3EditForm(CommonModelForm, OrganizationRequiredForm):
    class Meta:
        model = AbstractOrganizationSection3
        exclude = exclude
        widgets = {
            'financial_statement_review': forms.CheckboxInput(),
        }


# Section 4
class OrganizationSection4EditForm(CommonModelForm, OrganizationRequiredForm):
    class Meta:
        model = AbstractOrganizationSection4
        exclude = exclude
        widgets = {}


# Section 5
class OrganizationSection5EditForm(CommonModelForm, OrganizationRequiredForm):
    class Meta:
        model = AbstractOrganizationSection5
        exclude = exclude

        POSSIBLE_FORM_OF_FINANCIAL_SUPPORT_CHOICES = (
            ('1', _('Grant')),
            ('2', _('Loan')),
            ('3', _('Equity'))
        )

        widgets = {
            'possible_form_of_financial_support': PrettyCheckboxSelectMultiple(),
            'potential_use_of_investment': PrettyCheckboxSelectMultiple(),
            'possible_form_of_non_financial_support': PrettyCheckboxSelectMultiple()
        }


# Attachment
class OrganizationAttachmentForm(CommonModelForm, OrganizationRequiredForm):
    class Meta:
        model = AbstractOrganizationAttachment


class OrganizationAssistantshipForm(forms.Form):
    type_of_assistantship = forms.ModelChoiceField(
        required=False,
        queryset=TypeOfAssistantship.objects.all(),
        widget=forms.HiddenInput(),
    )

    type_of_assistantship_text = EnglishCharField(required=False, widget=forms.Textarea())
    is_required = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    description = EnglishCharField(required=False, widget=forms.Textarea())


class OrganizationParticipantForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    program = forms.ModelChoiceField(
        required=False,
        queryset=Program.objects.all(),
        widget=autocomplete_light.ChoiceWidget(ProgramInlineAutocomplete,
            attrs={'placeholder': _('Type for search programs by title.'), 'class': 'form-control'}
        )
    )
    month = forms.IntegerField(required=False, min_value=0, max_value=100,
                                                     widget=forms.NumberInput)
    status = forms.IntegerField(required=False, widget=forms.HiddenInput)

class ParticipantOrganizationForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    organization = forms.ModelChoiceField(
        required=False,
        queryset=Organization.objects.filter(type_of_organization=TYPE_STARTUP),
        widget=autocomplete_light.ChoiceWidget(OrganizationStartupAutocomplete,
            attrs={'placeholder': _('Type for search startup by title.'), 'class': 'form-control'}
        )
    )
    month = forms.IntegerField(required=False, min_value=0, max_value=100,
                                                     widget=forms.NumberInput)
    status = forms.IntegerField(required=False, widget=forms.HiddenInput)

class OrganizationFundingRoundForm(OrganizationRequiredForm):
    announced_date = forms.DateField(required=False, widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'),
                                                                          years=generate_year_range(next_years=10,
                                                                                                    prev_years=20)))
    closed_date = forms.DateField(required=False,
                                            widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'),
                                                                          years=generate_year_range(next_years=10,
                                                                                                    prev_years=20)))


class OrganizationEditForm(OrganizationRequiredForm, PermalinkForm):
    CHECKED_CHOICES = (
        (False, 'No'),
        (True, 'Yes'),
    )
    type_of_organization = EnglishCharField(required=False, max_length=50, widget=forms.HiddenInput())


    permalink = EnglishCharField()

    changed = forms.DateTimeField(required=False, widget=forms.HiddenInput)

    kind = forms.ChoiceField(
        label=_('What kind of your created ?'),
        required=False,
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

    key_person = forms.ModelMultipleChoiceField(
        required=False,
        queryset=OrganizationStaff.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(StaffAutocomplete,
                                                       attrs={'placeholder': _('Type for search people by name.'),
                                                              'class': 'form-control'}
                                                       )
    )

    staff = forms.ModelMultipleChoiceField(
        required=False,
        queryset=OrganizationStaff.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(StaffAutocomplete,
                                                       attrs={'placeholder': _('Type for search people by name.'),
                                                              'class': 'form-control'}
                                                       )
    )
    partners = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationPartnerAutocomplete,
            attrs={'placeholder': _('Type to search organizations by name.'), 'class': 'form-control'}
        )
    )
    government_partners = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationGovernmentPartnerAutocomplete,
            attrs={'placeholder': _('Type to search organizations by name.'), 'class': 'form-control'}
        )
    )
    media_partners = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationMediaPartnerAutocomplete,
            attrs={'placeholder': _('Type to search organizations by name.'), 'class': 'form-control'}
        )
    )
    association_partners = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationAssociationPartnerAutocomplete,
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

    programs = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Program.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(ProgramAutocomplete,
            attrs={'placeholder': _('Type for search programs by title.'), 'class': 'form-control'}
        )
    )

    jobs = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Job.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(JobAutocomplete,
            attrs={'placeholder': _('Type to search jobs by title.'), 'class': 'form-control'}
        )
    )

    in_the_news = forms.ModelMultipleChoiceField(
        required=False,
        queryset=InTheNews.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(InTheNewsAutocomplete,
            attrs={'placeholder': _('Type to search in the news by title.'), 'class': 'form-control'}
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
    cover_image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())
    images = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImagesWidget())

    name = EnglishCharField(max_length=255, widget=forms.TextInput())
    summary = EnglishCharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'maxlength': SUMMARY_MAX_LENGTH}))
    description = EnglishCharField(required=False, widget=CKEditorWidget())

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

    # investor_types = forms.ModelMultipleChoiceField(required=False, queryset=InvestorType.objects.all(),
    #                                                 widget=forms.CheckboxSelectMultiple(
    #                                                 attrs={'id': 'id_investor_types'}))

    investor_type = forms.ModelChoiceField(required=False, queryset=InvestorType.objects.all(),
                                            widget=forms.RadioSelect(
                                                attrs={'id': 'id_investor_type'}))

    topics = TreeNodeMultipleChoiceField(required=False, queryset=Topic.objects.all(), level_indicator=u'⌞', widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_topics'}))
    country = forms.ModelChoiceField(required=False, queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    product_launch = forms.ModelChoiceField(required=False, queryset=OrganizationProductLaunch.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    funding = forms.ModelChoiceField(required=False, queryset=OrganizationFunding.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    request_funding = forms.ModelChoiceField(required=False, queryset=OrganizationFunding.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    #deal_size_start = forms.IntegerField(required=False, min_value=0, max_value=1000000000, widget=forms.NumberInput)
    #deal_size_end = forms.IntegerField(required=False, min_value=0, max_value=1000000000, widget=forms.NumberInput)

    money_deal_size_start = MoneyField(required=False, max_digits=19, decimal_places=2)
    money_deal_size_end = MoneyField(required=False, max_digits=19, decimal_places=2)

    # External
    facebook_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Facebook URL')}))
    twitter_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Twitter URL')}))
    linkedin_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Linkedin URL')}))
    homepage_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Homepage URL')}))

    # Meta
    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=STATUS_CHOICES)
    specials = forms.ModelMultipleChoiceField(required=False, queryset=Special.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_specials'}))


    # 2018

    preferred_name = EnglishCharField(required=False, max_length=255, widget=forms.TextInput())
    company_registration_number = EnglishCharField(required=False, max_length=255, widget=forms.TextInput())

    date_of_establishment = forms.DateField(required=False,
                                            widget=BetterSelectDateWidget(empty_label=('Year', 'Month', ''),
                                                                          ignore_day=True,
                                                                          years=generate_year_range(next_years=1,
                                                                                                    prev_years=20)))

    is_register_to_nia = RequiredNullBooleanField(required=False, 
                                                  widget=forms.RadioSelect(choices=CHECKED_CHOICES))

    # specialty = EnglishCharField(required=False, widget=CKEditorWidget()
    specialty = MultiCharField(required=False, require_all_fields=False, validators=[english_validator])


    company_vision = EnglishCharField(required=False, widget=CKEditorWidget())
    company_mission = EnglishCharField(required=False, widget=CKEditorWidget())
    business_model = EnglishCharField(required=False, widget=CKEditorWidget())
    growth_strategy = EnglishCharField(required=False, widget=CKEditorWidget())

    office_type = forms.ModelMultipleChoiceField(required=False,
                                                  queryset=TypeOfOffice.objects.all(),
                                                  widget=PrettyCheckboxSelectMultiple)

    other_office_type = EnglishCharField(required=False, widget=forms.TextInput())

    focus_sector = forms.ModelMultipleChoiceField(required=False,
                                                  queryset=TypeOfFocusSector.objects.all(),
                                                  widget=PrettyCheckboxSelectMultiple)

    other_focus_sector = EnglishCharField(required=False, widget=forms.TextInput())

    focus_industry = forms.ModelMultipleChoiceField(required=False,
                                                    queryset=TypeOfFocusIndustry.objects.all(),
                                                    widget=PrettyCheckboxSelectMultiple)

    other_focus_industry = EnglishCharField(required=False, widget=forms.TextInput())

    stage_of_participants = forms.ModelMultipleChoiceField(required=False,
                                                           queryset=TypeOfStageOfParticipant.objects.all(),
                                                           widget=PrettyCheckboxSelectMultiple)

    has_participate_in_program = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    has_received_investment = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))

    financial_source = forms.ModelMultipleChoiceField(required=False,
                                                      queryset=TypeOfFinancialSource.objects.all(),
                                                      widget=PrettyCheckboxSelectMultiple)

    other_financial_source = EnglishCharField(required=False, widget=forms.TextInput())

    funding_type = forms.ModelMultipleChoiceField(required=False,
                                                  queryset=TypeOfFunding.objects.all(),
                                                  widget=PrettyCheckboxSelectMultiple)

    has_taken_equity_in_startup = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    taken_equity_amount = EnglishCharField(required=False,  widget=forms.TextInput())
    #money_taken_equity_amount = MoneyField(required=False, max_digits=19, decimal_places=2)

    is_lead_investor = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    has_taken_equity_in_fund_organization = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))

    money_money_raise = MoneyField(required=False, max_digits=19, decimal_places=2)
    money_target_funding = MoneyField(required=False, max_digits=19, decimal_places=2)
    money_pre_money_valuation = MoneyField(required=False, max_digits=19, decimal_places=2)
    money_amount_of_money_invested = MoneyField(required=False, max_digits=19, decimal_places=2)

    instagram_url = forms.URLField(required=False,
                                   widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Instagram URL')}))
    other_channel = EnglishCharField(required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control last', 'placeholder': _('Other Channel')}))

    attachments_types = forms.ModelMultipleChoiceField(required=False,
                                                       queryset=TypeOfAttachment.objects.filter(
                                                           attachment_for=TYPE_STARTUP),
                                                       widget=PrettyCheckboxSelectMultiple)

    attachments = files_widget.forms.FilesFormField(
        required=False,
        fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False),),
        widget=files_widget.forms.widgets.FilesWidget()
    )

    def __init__(self, inst=None, model=None, request_user=None, *args, **kwargs):


        super(OrganizationEditForm, self).__init__(inst, model, request_user, *args, **kwargs)


        if inst.type_of_organization in [inst.TYPE_SOCIAL_ENTERPRISE, inst.TYPE_STARTUP]:

            self.fields['growth_stage'] = forms.ModelChoiceField(required=False, queryset=OrganizationGrowthStage.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

        elif inst.type_of_organization in [inst.TYPE_INVESTOR, inst.TYPE_SUPPORTING_ORGANIZATION]:

            self.fields['growth_stage'] = forms.ModelMultipleChoiceField(
                required=False,
                queryset=OrganizationGrowthStage.objects.all(),
                widget=forms.CheckboxSelectMultiple(
                attrs={'id': 'id_growth_stage'})
            )

            self.fields['attachments_types'] = forms.ModelMultipleChoiceField(
                required=self.fields['attachments_types'].required,
                queryset=TypeOfAttachment.objects.filter(attachment_for=TYPE_INVESTOR),
                widget=PrettyCheckboxSelectMultiple)

        self.fields['partners'].widget.instance = inst

    '''
    def clean(self):

        cleaned_data = super(OrganizationEditForm, self).clean()

        # bypass check required
        if self.request_user and self.request_user.is_editor:
            return cleaned_data


        for role in cleaned_data['organization_roles'].all():

            field_name = '%s_types' % role.permalink

            if role.permalink == Organization.TYPE_SUPPORTING_ORGANIZATION:
                self.fields['organization_types'].required = False
                self.fields['type_of_supports'].required = False
                self.validate_required_field(cleaned_data, 'organization_types')
                self.validate_required_field(cleaned_data, 'type_of_supports')

            else:
                field = self.fields.get(field_name)
                if field:
                    field.required = True

                self.validate_required_field(cleaned_data, field_name)

        return cleaned_data
    '''

    def validate_required_field(self, cleaned_data, field_name, message="This field is required"):
        if (field_name in cleaned_data and (cleaned_data[field_name] is None)):
            self._errors[field_name] = self.error_class([message])

            del cleaned_data[field_name]

class OrganizationEditInlineForm(CommonForm):
    type_of_organization = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'id': 'id_type_of_organization'}), choices=Organization.EXPAND_TYPE_CHOICES)

    organization_type__permalink = forms.CharField(required=False, widget=forms.HiddenInput)

    name = EnglishCharField(max_length=255, widget=forms.TextInput())
    image = files_widget.forms.FilesFormField(required=False, fields=(
        forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ),
                                              widget=files_widget.forms.widgets.ImageWidget())

    location_of_organizations_headquarters = EnglishCharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    store_email_of_organizations_headquarters = forms.EmailField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))



class JobEditForm(CommonForm):


    def __init__(self, *args, **kwargs):
        try:
            user = kwargs.pop('user')
        except KeyError:
            user = None

        try:
            required_organization = kwargs.pop('required_organization')
        except KeyError:
            required_organization = False

        super(JobEditForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['organization'].queryset = Organization.objects.filter(Q(admins=user)|Q(created_by=user)).filter(program__isnull=True)

        self.fields['organization'].required = required_organization


    YEARS_OF_EXPERIENCE_CHOICES = (
        (None, 'Select Years of Experience...'),
        (0, '0+'),
        (1, '1+'),
        (2, '2+'),
        (3, '3+'),
        (4, '4+'),
        (5, '5+'),
        (6, '6+'),
        (7, '7+'),
        (8, '8+'),
        (9, '9+'),
        (10, '10+'),
    )


    title = EnglishCharField(max_length=255, widget=forms.TextInput())
    contact_information = EnglishCharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    description = EnglishCharField(required=False, widget=CKEditorWidget(config_name='default'))


    role = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}), choices=Job.ROLE_CHOICES)

    job_primary_role = TreeNodeChoiceField(required=True, queryset=JobRole.objects.all(), level_indicator=u'⌞', widget=forms.Select(attrs={'class': 'form-control'}))
    job_roles = TreeNodeMultipleChoiceField(required=False, queryset=JobRole.objects.all(), level_indicator=u'⌞', widget=PrettyCheckboxSelectMultiple())

    position = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'form-control'}), choices=Job.POSITION_CHOICES)

    # salary_min = forms.IntegerField(required=False, min_value=0, max_value=1000000000)
    # salary_max = forms.IntegerField(required=False, min_value=0, max_value=1000000000)

    money_salary_min = MoneyField(required=False, max_digits=19, decimal_places=2)
    money_salary_max = MoneyField(required=False, max_digits=19, decimal_places=2)

    equity_min = forms.DecimalField(required=False, min_value=0, max_value=1000000000, max_digits=10, decimal_places=2)
    equity_max = forms.DecimalField(required=False, min_value=0, max_value=1000000000, max_digits=10, decimal_places=2)

    remote = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'id': 'id_remote'}), choices=Job.REMOTE_CHOICES)
    years_of_experience = forms.IntegerField(required=False, widget=forms.Select(attrs={'class': 'form-control'}, choices=YEARS_OF_EXPERIENCE_CHOICES))

    country = forms.ModelChoiceField(required=False, queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    location = EnglishCharField(required=False, max_length=255, widget=forms.TextInput())
    locations = forms.ModelMultipleChoiceField(required=False, queryset=Location.objects.all(), widget=PrettyCheckboxSelectMultiple())

    skills = TagField(required=False, widget=TagAutocompleteTagIt(max_tags=False))

    status = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'id_status'}), choices=Job.STATUS_CHOICES, initial=STATUS_PUBLISHED)

    organization = forms.ModelChoiceField(required=False, queryset=Organization.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))


class ProgramEditForm(OrganizationRequiredForm, PermalinkForm):
    CHECKED_CHOICES = (
        (False, 'No'),
        (True, 'Yes'),
    )
    name = EnglishCharField(max_length=255, widget=forms.TextInput())

    permalink = EnglishCharField(required=False)

    cover_image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False),),
                                                    widget=files_widget.forms.widgets.ImageWidget())

    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False),), widget=files_widget.forms.widgets.ImageWidget())
    description = EnglishCharField(required=False, widget=CKEditorWidget())

    program_type = forms.ModelMultipleChoiceField(required=False,
                                                  queryset=ProgramType.objects.all(),
                                                  widget=PrettyCheckboxSelectMultiple)

    date_of_establishment = forms.DateField(required=False,
                                            widget=BetterSelectDateWidget(empty_label=('Year', 'Month', ''),
                                                                          ignore_day=True,
                                                                          years=generate_year_range(next_years=5, prev_years=7)))

    focus_sector = forms.ModelMultipleChoiceField(required=False,
                                                  queryset=TypeOfFocusSector.objects.all(),
                                                  widget=PrettyCheckboxSelectMultiple)

    other_focus_sector = EnglishCharField(required=False, widget=forms.TextInput())

    focus_industry = forms.ModelMultipleChoiceField(required=False,
                                                    queryset=TypeOfFocusIndustry.objects.all(),
                                                    widget=PrettyCheckboxSelectMultiple)

    other_focus_industry = EnglishCharField(required=False, widget=forms.TextInput())

    stage_of_participants = forms.ModelMultipleChoiceField(required=False,
                                                           queryset=TypeOfStageOfParticipant.objects.all(),
                                                           widget=PrettyCheckboxSelectMultiple)

    organization = forms.ModelChoiceField(required=True,
                                          queryset=Organization.objects.none(),
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    is_acting_as_an_investor = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    has_invited_in_participants_team = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))

    investment_type = forms.ModelMultipleChoiceField(required=False,
                                                     queryset=TypeOfInvestment.objects.all(),
                                                     widget=PrettyCheckboxSelectMultiple)

    investment_stage_type = forms.ModelMultipleChoiceField(required=False,
                                                           queryset=TypeOfInvestmentStage.objects.all(),
                                                           widget=PrettyCheckboxSelectMultiple)

    specific_stage = EnglishCharField(required=False, widget=forms.TextInput())
    has_taken_equity_in_participating_team = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    does_provide_financial_supports = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))

    amount_of_financial_supports = EnglishCharField(required=False, max_length=255, widget=forms.TextInput())
    period_of_engagement = forms.IntegerField(required=False, widget=forms.TextInput())

    does_provide_working_spaces = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    is_own_working_space = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))

    does_provide_service_and_facility = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    specify_service = MultiCharField(required=False, require_all_fields=False, validators=[english_validator])

    mentor = forms.ModelMultipleChoiceField(
        required=False,
        queryset=OrganizationStaff.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(StaffAutocomplete,
                                                       attrs={'placeholder': _('Type for search people by name.'),
                                                              'class': 'form-control'}
                                                       )
    )

    staff = forms.ModelMultipleChoiceField(
        required=False,
        queryset=OrganizationStaff.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(StaffAutocomplete,
                                                       attrs={'placeholder': _('Type for search people by name.'),
                                                              'class': 'form-control'}
                                                       )
    )

    attachments_types = forms.ModelMultipleChoiceField(required=False,
                                                       queryset=TypeOfAttachment.objects.filter(attachment_for=TYPE_PROGRAM),
                                                       widget=PrettyCheckboxSelectMultiple)

    other_attachments_types = EnglishCharField(required=False, widget=forms.TextInput(), max_length=1024)

    attachments = files_widget.forms.FilesFormField(
        required=False,
        fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ),
        widget=files_widget.forms.widgets.FilesWidget()
    )

    status = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_status'}),
                               choices=STATUS_CHOICES)

    # External
    facebook_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control last', 'placeholder': _('Facebook URL')}))
    twitter_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control last', 'placeholder': _('Twitter URL')}))
    linkedin_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control last', 'placeholder': _('Linkedin URL')}))
    homepage_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control last', 'placeholder': _('Homepage URL')}))

    instagram_url = forms.URLField(required=False,
                                   widget=forms.URLInput(
                                       attrs={'class': 'form-control last', 'placeholder': _('Instagram URL')}))
    other_channel = EnglishCharField(required=False,
                                    widget=forms.Textarea(
                                        attrs={'class': 'form-control last', 'placeholder': _('Other Channel')}))

    admins = forms.ModelMultipleChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(UserAdminAutocomplete,
            attrs={'placeholder': _('Type to search people by name.'), 'class': 'form-control'}
        )
    )

    partners = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(OrganizationPartnerAutocomplete,
                                                       attrs={'placeholder': _('Type to search organizations by name.'),
                                                              'class': 'form-control'}
                                                       )
    )

    is_partner = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))
    is_register_to_nia = RequiredNullBooleanField(required=False, widget=forms.RadioSelect(choices=CHECKED_CHOICES))

    def __init__(self, inst=None, model=None, request_user=None, *args, **kwargs):
        super(ProgramEditForm, self).__init__(inst, model, request_user, *args, **kwargs)


        if request_user and request_user.id:
            condition = (Q(admins=request_user)|Q(created_by=request_user))&Q(type_of_organization=TYPE_SUPPORTING_ORGANIZATION)&Q(program__isnull=True)
            if inst and inst.organization:
                condition = condition | Q(id=inst.organization.id)

            self.fields['organization'].queryset = Organization.objects.filter(condition).extra(select={'name': "CONCAT(name, '|||', status)", 'is_published': 'status = %d' % STATUS_PUBLISHED, 'is_pending': 'status = %d' % STATUS_PENDING}).order_by('-is_published', '-is_pending')
        elif inst and inst.organization:
            self.fields['organization'].queryset = Organization.objects.filter(id=inst.organization.id)

        if inst and inst.id:
            self.fields['programs'] = forms.ModelMultipleChoiceField(
                required=False,
                queryset=Program.objects.filter(organization=inst),
                widget=autocomplete_light.MultipleChoiceWidget(ProgramAutocomplete,
                   attrs={'placeholder': _('Type for search programs by title.'),  'class': 'form-control'})
            )
            self.fields['permalink'].required = True

        # self.fields['partners'].widget.form_instance = self
        self.fields['partners'].widget.instance = inst


class ProgramInlineEditForm(CommonForm):
    name = EnglishCharField(max_length=255, widget=forms.TextInput())

class BatchSection1Form(OrganizationRequiredForm):
    title = EnglishCharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Title')}))

    amount_pre_seed_stage = EnglishCharField(required=False)
    amount_seed_stage = EnglishCharField(required=False)
    amount_pre_series_a_stage = EnglishCharField(required=False)

    amount_series_a_stage = EnglishCharField(required=False)
    amount_series_b_stage = EnglishCharField(required=False)
    amount_series_c_stage = EnglishCharField(required=False)

    amount_specific_stage = EnglishCharField(required=False)
    amount_total_stage = EnglishCharField(required=False)


class BatchSection2Form(OrganizationRequiredForm):
    title = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Title')}))

    total_teams_applying = EnglishCharField(required=False)
    total_teams_accepted = EnglishCharField(required=False)
    total_participants_accepted = EnglishCharField(required=False)
    total_graduated_teams_accepted = EnglishCharField(required=False)

    total_training_program = EnglishCharField(required=False)
    total_organized_event = EnglishCharField(required=False)

    total_coached_staff = EnglishCharField(required=False)
    total_assisting_staff = EnglishCharField(required=False)

    total_approximated_products = EnglishCharField(required=False)


class ContactInformationForm(OrganizationRequiredForm):
    address = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Office Address'), 'readonly': 'readonly'}))
    mobile = EnglishCharField(required=False, max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Mobile'), 'readonly': 'readonly'}))
    email = forms.EmailField(max_length=75, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Email'), 'readonly': 'readonly'}))
    tel = EnglishCharField(required=False, max_length=128,
                      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Tel')}))


class OrganizationInformationForm(ContactInformationForm):
    name = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Name'), 'readonly': 'readonly'}))
    register_number = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Company Registration Number'), 'readonly': 'readonly'}))


class ContactPersonInformationForm(forms.Form):
    name = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}))
    job_title = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Job Title')}))

    email = forms.EmailField(max_length=75, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Email')}))
    tel = EnglishCharField(required=False, max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Tel')}))
    mobile = EnglishCharField(required=False, max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Mobile')}))


class StaffInviteForm(InviteForm):
    status = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Staff staus')}))
    contact_number = EnglishCharField(required=False, max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Contact number')}))
    attachments = files_widget.forms.FilesFormField(
        required=False,
        fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False),),
        widget=files_widget.forms.widgets.FilesWidget()
    )

    staff = None

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None, extra_context=None):

        super(StaffInviteForm, self).save(
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

        email = self.cleaned_data.get('email')
        user = User.objects.get(email=email)

        staff, created = OrganizationStaff.objects.get_or_create(
            email=self.cleaned_data.get('email'),
            job_title=self.cleaned_data.get('summary'),
            contact_number=self.cleaned_data.get('contact_number'),
            attachments=self.cleaned_data.get('attachments'),
            user=user
        )

        self.staff = staff

    def clean_email(self):
        email = self.cleaned_data.get('email')
        UserModel = get_user_model()
        if UserModel.objects.filter(email=email).exists():
            pass

        return email


class OrganizationExtraForm(OrganizationRequiredForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Prefer not to say'),
    )

    gender = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'id': 'id_gender'}), choices=GENDER_CHOICES)
    nationality = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country_of_birth = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    id_card = EnglishCharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    issued_at = EnglishCharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    date_of_birth = forms.DateField(required=False,  widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'),
                                                                                   years=generate_year_range(next_years=1, prev_years=100)))
    date_of_issued_date = forms.DateField(required=False, widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'),
                                                                                       years=generate_year_range(next_years=1, prev_years=100)))

    expired_date = forms.DateField(required=False, widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'),
                                                                                 years=generate_year_range(next_years=10,
                                                                                                           prev_years=100)))

    number_of_employees = forms.IntegerField(required=False)


class JobApplyForm(forms.Form):
    job = forms.ModelChoiceField(queryset=Job.objects.all(), widget=forms.HiddenInput)
    message = forms.CharField(required=False, max_length=1000, widget=forms.Textarea)


# Formset
class TeamInformationForm(forms.Form):
    name = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first', 'placeholder': _('Name')}))
    title = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control last', 'placeholder': _('Title')}))

class PhoneNumberOfOrganizationsHeadquartersForm(OrganizationRequiredForm):
    phone_number = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Phone Number')}))

class LocationOfOrganizationsOperatingFacilitiesForm(forms.Form):
    address = EnglishCharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control first last', 'placeholder': _('Address'), 'rows': 2}))

class MeasurementYearValuesForm(forms.Form):
    year_of_datapoint = EnglishCharField(required=True, widget=forms.Select(choices=generate_year_range(choices=True, empty_label=_('Year of Datapoint')), attrs={'class': 'form-control first last', 'placeholder': _('Year of datapoint')}))
    value_of_impact_1 = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Value of impact 1')}))
    value_of_impact_2 = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Value of impact 2')}))
    value_of_impact_3 = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control first last', 'placeholder': _('Value of impact 3')}))

class Top3MajorInvestorsYearAndAmountForm(forms.Form):
    title = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control last', 'placeholder': _('Investor name, years, amounts')}))

class Top3MajorDonorsYearAndAmountForm(forms.Form):
    title = EnglishCharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control last', 'placeholder': _('Donor name, years, amounts')}))


class InTheNewsEditForm(CommonForm):

    title = EnglishCharField(max_length=1024, widget=forms.TextInput())
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': _('News URL')}))
    date = forms.DateField(required=False, widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'), years=generate_year_range(next_years=1, prev_years=10)))
    description = EnglishCharField(required=False, widget=forms.Textarea())
    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())
