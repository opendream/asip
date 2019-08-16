from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import CommonForm, EnglishCharField
import files_widget


class PortfolioEditForm(CommonForm):

    title = EnglishCharField(max_length=255, widget=forms.TextInput())
    images = files_widget.forms.FilesFormField(
        required=True,
        fields=(forms.CharField(required=False), forms.CharField(required=False), forms.CharField(required=False), ),
        widget=files_widget.forms.widgets.ImagesWidget()
    )
    description = EnglishCharField(required=False, widget=CKEditorWidget(config_name='minimal'))
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control last', 'placeholder': _('Portfolio URL')}))

