import autocomplete_light
from django import forms
from django.utils.translation import ugettext_lazy as _
from account.models import User

from common.constants import SUMMARY_MAX_LENGTH

from common.forms import CommonForm, BetterSelectDateWidget, EnglishCharField
from djmoney.forms import MoneyField
import files_widget
from organization.models import Organization
from party.models import Party
from relation.autocomplete_light_registry import OrganizationExperienceAutocomplete, PartyReceivedFundingAutocomplete, \
    UserAdminAutocomplete, UserReceiverAutocomplete


class ExperienceEditForm(CommonForm):

    dst = forms.ModelChoiceField(
        required=True,
        queryset=Organization.objects.all(),
        widget=autocomplete_light.ChoiceWidget(OrganizationExperienceAutocomplete,
                                                       attrs={'placeholder': _('Type for search organizations by name'),
                                                              'class': 'form-control'}
        )
    )

    title = EnglishCharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'CEO, Lead Developer, etc.'}))
    description = EnglishCharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'maxlength': SUMMARY_MAX_LENGTH, 'placeholder': 'What did you do? What were your accomplishments?'}))

    start_date = forms.DateField(required=True, widget=BetterSelectDateWidget(
        empty_label=('Year', 'Month', 'Day'),
        ignore_day=True,
        attrs={'class': 'form-control'}
    ))
    end_date = forms.DateField(required=False, widget=BetterSelectDateWidget(
        empty_label=('Year', 'Month', 'Day'),
        ignore_day=True,
        attrs={'class': 'form-control'}
    ))

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data['end_date']

        if not start_date or (start_date and end_date and start_date > end_date):
            raise forms.ValidationError('The end date must be greater than the start date.')


        return end_date


class ReceivedFundingEditForm(CommonForm):

    dst = forms.ModelChoiceField(
        required=True,
        queryset=Party.objects.all(),
        widget=autocomplete_light.ChoiceWidget(PartyReceivedFundingAutocomplete,
                                               attrs={'placeholder': _('Type for search supporter by name'),
                                                      'class': 'form-control'}
        )
    )

    #amount = forms.DecimalField()
    money_amount = MoneyField(required=True, max_digits=19, decimal_places=2)

    title = EnglishCharField(required=False, max_length=255, widget=forms.TextInput(attrs={'placeholder': ''}))

    date = forms.DateField(required=True, widget=BetterSelectDateWidget(
        empty_label=('Year', 'Month', 'Day'),
        attrs={'class': 'form-control'}
    ))


class InviteTestifyEditForm(CommonForm):

    receivers = forms.ModelMultipleChoiceField(
        required=True,
        queryset=User.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(UserReceiverAutocomplete,
            attrs={'placeholder': _('Type to search people by name.'), 'class': 'form-control'}
        )
    )

    message = EnglishCharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Your invites message'}))

