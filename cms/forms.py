# -*- coding: utf-8 -*-

import autocomplete_light
from mptt.forms import TreeNodeMultipleChoiceField
from tagging.forms import TagField
from ckeditor.widgets import CKEditorWidget
from cms.models import News, Event, CommonCms
from django import forms
from django.utils.translation import ugettext_lazy as _
from common.constants import SUMMARY_MAX_LENGTH
from common.forms import PermalinkForm, BetterSelectDateWidget
from common.functions import generate_year_range
import files_widget
from organization.models import Organization
from party.models import Party
from relation.autocomplete_light_registry import CmsHasPartyAutocomplete
from tagging_autocomplete_tagit.widgets import TagAutocompleteTagIt
from taxonomy.models import Topic, ArticleCategory


class CmsForm(PermalinkForm):

    class Meta:
        model = CommonCms

    title = forms.CharField(max_length=512, help_text=_('Title in 512 characters'))
    image = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.ImageWidget())
    permalink = forms.CharField()
    summary = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'maxlength': 240}))
    description = forms.CharField(required=False, widget=CKEditorWidget())
    topics = forms.ModelMultipleChoiceField(queryset=Topic.objects.filter(level=0), widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_topics'}))

    tags = TagField(required=False, widget=TagAutocompleteTagIt(max_tags=False), help_text='')

    in_the_news = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Party.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget(CmsHasPartyAutocomplete,
            attrs={'placeholder': _('Type to search organizations or people by name.'), 'class': 'form-control'}
        )
    )

    is_promoted = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'id_is_promoted'})
    )


class NewsForm (CmsForm):

    class Meta:
        model = News
    # Relation
    #organization = forms.ModelChoiceField(queryset=Organization.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    # deprecate
    article_category = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'form-control'}), choices=News.ARTICLE_TYPE_CHOICES)

    categories = TreeNodeMultipleChoiceField(queryset=ArticleCategory.objects.all(), level_indicator=u'⌞', widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_categories'}))

    facebook_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Facebook URL')}))
    twitter_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Twitter URL')}))
    homepage_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Homepage URL')}))

    files = files_widget.forms.FilesFormField(required=False, fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ), widget=files_widget.forms.widgets.FilesWidget())


class EventForm (CmsForm):

    class Meta:
        model = Event
    # Relation
    #organization = forms.ModelChoiceField(queryset=Organization.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    location = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':2}), help_text='Location of event')
    start_date = forms.DateField(required=True, widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'), years=generate_year_range(next_years=5, prev_years=7)))
    end_date = forms.DateField(required=False, widget=BetterSelectDateWidget(empty_label=('Year', 'Month', 'Day'),years=generate_year_range(next_years=5, prev_years=7)))
    time = forms.CharField(required=False, max_length=255, widget=forms.TextInput())

    phone = forms.CharField(required=False, max_length=128, widget=forms.TextInput(), help_text='You can add more than one telephone number. Use a comma to separate each number.')
    email = forms.EmailField(max_length=75, required=False)
    facebook_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Facebook URL')}))
    twitter_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Twitter URL')}))
    homepage_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Homepage URL')}))

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date is not None and start_date > end_date:
            raise forms.ValidationError('The end date must be greater than the start date.')

        return end_date

