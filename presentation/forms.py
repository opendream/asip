import autocomplete_light
from django import forms



class QueueForm(forms.Form):

    adds = forms.ModelMultipleChoiceField(None,
        required=False,
        widget=autocomplete_light.MultipleChoiceWidget(attrs={'class': 'form-control'}),
    )

    def __init__(self, queryset=None, autocomplete=None, label=None, placeholder=None,  *args, **kwargs):

        autocomplete.choices = queryset

        self.base_fields['adds'].queryset = queryset
        self.base_fields['adds'].widget.autocomplete=autocomplete
        self.base_fields['adds'].label = label
        self.base_fields['adds'].widget.attrs['placeholder'] = placeholder
        super(QueueForm, self).__init__(*args, **kwargs)
        self.fields['adds'].help_text = None
