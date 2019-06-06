import datetime
from decimal import Decimal
from django import forms
from django.conf import settings
from django.core import validators
from django.db import models
from django.forms import Widget, Select, ChoiceField
from django.forms.extras import SelectDateWidget
from django.forms.extras.widgets import RE_DATE
from django.utils import datetime_safe
from django.utils.dates import MONTHS
from django.utils.formats import get_format
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from django.utils import six
from django.utils.encoding import force_text, force_str
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils import timezone

import re
from mptt.forms import TreeNodeMultipleChoiceField
from common.functions import generate_year_range
from common.validators import validate_reserved_url
from multiselectfield import MultiSelectFormField


class CommonForm(forms.Form):

    def __init__(self, inst=None, model=None, request_user=None, *args, **kwargs):
        super(CommonForm, self).__init__(*args, **kwargs)
        self.inst = inst
        self.model = model
        self.request_user = request_user


    def is_new(self):

        if self.inst and self.inst.id:
            return False

        return True


class PermalinkForm(CommonForm):

    PERMALINK_FIELDS = ['permalink']

    def __init__(self, inst=None, model=None, request_user=None, *args, **kwargs):
        super(PermalinkForm, self).__init__(inst, model, request_user, *args, **kwargs)

        for field_name in self.PERMALINK_FIELDS:
            if self.fields[field_name].max_length > 255:
                self.fields[field_name].max_length = 255

            if 'mail' in field_name:
                self.fields[field_name].validators.append(validators.RegexValidator(re.compile('^[\w.+@-]+$'), _('Enter a valid permalink.'), 'invalid'))
                self.fields[field_name].help_text = _(
                    'Required unique 30 characters or fewer. Letters, numbers and ./-/+/@/_ characters')

            else:
                self.fields[field_name].validators.append(validators.RegexValidator(re.compile('^[\w.-]+$'), _('Enter a valid permalink.'), 'invalid'))
                self.fields[field_name].help_text = _('Required unique 30 characters or fewer. Letters, numbers and ./-/_ characters')

    def clean(self):

        cleaned_data = super(PermalinkForm, self).clean()

        for field_name in self.PERMALINK_FIELDS:
            permalink = cleaned_data.get(field_name, '')


            if self.model.objects.filter(**{'%s__iexact' % field_name: permalink}).exclude(id=self.inst.id).count() > 0 or not validate_reserved_url(permalink, True):

                if not self._errors.has_key(field_name):
                    self._errors[field_name] = ErrorList()

                self._errors[field_name].append(_('This %s is already in use.') % _(field_name))

        return cleaned_data



class CommonModelForm(forms.ModelForm):

    #error_css_class = 'errors alert alert-danger'

    def __init__(self, *args, **kwargs):

        kwargs.setdefault('label_suffix', '')
        instance = kwargs.get('instance')

        for field_name, field in self.base_fields.iteritems():
            # Fixed 2 digits decimal field
            if type(field) is forms.DecimalField:
                instance_values = getattr(instance, field_name)
                if instance_values:
                    instance_values = instance_values.quantize(Decimal('0.01'))
                    setattr(instance, field_name, instance_values)


        super(CommonModelForm, self).__init__(*args, **kwargs)


        for field_name, field in self.fields.iteritems():

            try:
                field_class = field.widget.attrs['class']
            except:
                field_class = ''

            field_class = field_class.split()
            field_class.append('form-control')

            #print type(field)


            # Fixed label from Django ModelMultipleChoiceField
            if type(field) is forms.ModelMultipleChoiceField or type(field) is TreeNodeMultipleChoiceField:
                try:
                    field.label = self._meta.model._meta.get_field_by_name(field_name)[0].verbose_name
                except:
                    pass

            # Add select other value from MultiSelectFormField
            if type(field) is MultiSelectFormField:

                field_class.append('select-with-other')
                instance_values = getattr(instance, field_name)
                if instance_values:
                    choices = field.choices
                    value_choices = zip(*choices)[0]
                    other_value = list(set(instance_values) - set(value_choices))

                    if len(other_value):
                        other_value = other_value[0]
                    else:
                        other_value = False

                    if 'other' in choices[-1][0].lower() and other_value:
                        other_choice = choices.pop()
                        choices.append((other_value, other_choice[1]))
                        field.choices = choices
                        self.fields[field_name] = field


            # Fixed 2 digits decimal field
            field.suffix = ''
            model_field = self._meta.model._meta.get_field_by_name(field_name)[0]
            if hasattr(model_field, 'suffix'):
                field.suffix = model_field.suffix

            if type(field) is forms.DecimalField:
                # field_class.append('input-price')
                field.decimal_places = 2



            field.widget.attrs['class'] = ' '.join(field_class).strip()

            # re init again for force 2 digits decimal field
            #super(CommonModelForm, self).__init__(*args, **kwargs)



    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': force_text(e)}
                         for e in bf_errors])
                hidden_fields.append(six.text_type(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                css_classes = css_classes.split(' ')
                css_classes.append('controls')
                css_classes.append('form-group')
                css_classes.append('group-field-name')
                css_classes.append('field-name-%s' % name)
                if 'date' in name:
                    css_classes.append('field-type-date')

                extra_class = ''
                if field.suffix:
                    extra_class = ' field-has-suffix'
                    suffix = '<span class="field-suffix">%s</span>' % force_text(field.suffix)
                else:
                    suffix = ''

                css_classes = ' '.join(css_classes).strip()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_text(bf_errors))

                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    label = bf.label_tag(label, attrs={'class': 'field-container control-label'}) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_text(field.help_text)
                else:
                    help_text = ''

                if bf_errors:
                    bf_errors = '<div class="errors alert alert-danger">%s</div>' % bf_errors


                output.append(normal_row % {
                    'errors': force_text(bf_errors),
                    'label': force_text(label),
                    'field': six.text_type(bf),
                    'suffix': suffix,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'field_name': bf.html_name,
                    'extra_class':extra_class,
                })

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text': '',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))

    def as_bootstrap(self):
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            normal_row='<div%(html_class_attr)s>%(label)s<div class="field-container%(extra_class)s">%(field)s%(suffix)s%(help_text)s%(errors)s</div></div>',
            error_row='<li>%s</li>',
            row_ender='</div>',
            help_text_html=' <span class="help-block">%s</span>',
            errors_on_separate_row=False)

    def clean(self):

        cleaned_data = super(CommonModelForm, self).clean()

        if hasattr(self, 'PERMALINK_FIELDS'):

            for field_name in self.PERMALINK_FIELDS:
                permalink = cleaned_data.get(field_name, '')

                if self._meta.model.objects.filter(**{'%s__iexact' % field_name: permalink}).exclude(
                        id=self.instance.id).count() > 0 or not validate_reserved_url(permalink, True):

                    if not self._errors.has_key(field_name):
                        self._errors[field_name] = ErrorList()

                    self._errors[field_name].append(_('This %s is already in use.') % _(field_name))

        return cleaned_data


class PrettyChoiceInput(object):


    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.id_for_label:
            label_for = format_html(' for="{0}"', self.id_for_label)
        else:
            label_for = ''
        output = format_html('{1} <label{0}>{2}</label>', label_for, self.tag(), self.choice_label)

        return output

class PrettyRadioChoiceInput(PrettyChoiceInput, forms.widgets.RadioChoiceInput):
    pass

class PrettyCheckboxChoiceInput(PrettyChoiceInput, forms.widgets.CheckboxChoiceInput):
    pass


class PrettyFieldRenderer(forms.widgets.RadioFieldRenderer):

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id', None)
        start_tag = format_html('<ul id="{0}">', id_) if id_ else '<ul>'
        output = [start_tag]
        for i, choice in enumerate(self.choices):

            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{0}'.format(i)
                sub_ul_renderer = forms.widgets.ChoiceFieldRenderer(name=self.name,
                                                      value=self.value,
                                                      attrs=attrs_plus,
                                                      choices=choice_label)
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html('<li>{0}{1}</li>', choice_value,
                                          sub_ul_renderer.render()))
            else:
                w = self.choice_input_class(self.name, self.value,
                                            self.attrs.copy(), choice, i)
                #output.append(format_html('<li>{0}</li>', force_text(w)))
                output.append('<li>%s</li>' % w)
        output.append('</ul>')

        return mark_safe('\n'.join(output))

class PrettyRadioFieldRenderer(PrettyFieldRenderer, forms.widgets.RadioFieldRenderer):
    choice_input_class = PrettyRadioChoiceInput

class PrettyCheckboxFieldRenderer(PrettyFieldRenderer, forms.widgets.CheckboxFieldRenderer):
    choice_input_class = PrettyCheckboxChoiceInput


class PrettyRadioSelect(forms.widgets.RadioSelect):
    renderer = PrettyRadioFieldRenderer

    def id_for_label(self, id_):
        return id_

class PrettyCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    renderer = PrettyCheckboxFieldRenderer


    def id_for_label(self, id_):
        return '%s' % id_


def _parse_date_fmt():
    fmt = get_format('DATE_FORMAT')
    escaped = False
    for char in fmt:
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif char in 'Yy':
            yield 'year'
        elif char in 'bEFMmNn':
            yield 'month'
        elif char in 'dj':
            yield 'day'


class BetterSelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.
    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = (0, '---')
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, months=None, empty_label=None, ignore_day=False):
        self.attrs = attrs or {}

        # Optional list or tuple of years to use in the "year" select box.
        if years:
            self.years = years
        else:
            self.years = generate_year_range()
        # Optional dict of months to use in the "month" select box.
        if months:
            self.months = months
        else:
            self.months = MONTHS

        self.ignore_day = ignore_day

        # Optional string, list, or tuple to use as empty_label.
        if isinstance(empty_label, (list, tuple)):
            if not len(empty_label) == 3:
                raise ValueError('empty_label list/tuple must have 3 elements.')

            self.year_none_value = (0, empty_label[0])
            self.month_none_value = (0, empty_label[1])
            self.day_none_value = (0, empty_label[2])
        else:
            if empty_label is not None:
                self.none_value = (0, empty_label)

            self.year_none_value = self.none_value
            self.month_none_value = self.none_value
            self.day_none_value = self.none_value

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, six.string_types):
                if settings.USE_L10N:
                    try:
                        input_format = get_format('DATE_INPUT_FORMATS')[0]
                        v = datetime.datetime.strptime(force_str(value), input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = [int(v) for v in match.groups()]
        html = {}
        choices = [(i, i) for i in self.years]
        html['year'] = self.create_select(name, self.year_field, value, year_val, choices, self.year_none_value)
        choices = list(six.iteritems(self.months))
        html['month'] = self.create_select(name, self.month_field, value, month_val, choices, self.month_none_value)
        choices = [(i, i) for i in range(1, 32)]
        html['day'] = self.create_select(name, self.day_field, value, day_val, choices, self.day_none_value)

        output = []
        for field in _parse_date_fmt():
            if self.ignore_day and field == 'day':
                output.append('<span class="select-date-wrapper hidden">%s</span>' % html[field])
            else:
                output.append('<span class="select-date-wrapper">%s</span>' % html[field])
        return mark_safe('\n'.join(output))

    def id_for_label(self, id_):
        for first_select in _parse_date_fmt():
            return '%s_%s' % (id_, first_select)
        else:
            return '%s_month' % id_

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None
        if y and m and d:
            if settings.USE_L10N:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    date_value = datetime.date(int(y), int(m), int(d))
                except ValueError:
                    return '%s-%s-%s' % (y, m, d)
                else:
                    date_value = datetime_safe.new_date(date_value)
                    return date_value.strftime(input_format)
            else:
                return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)

    def create_select(self, name, field, value, val, choices, none_value):
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        if not self.is_required:
            choices.insert(0, none_value)
        local_attrs = self.build_attrs(id=field % id_)
        s = Select(choices=choices)
        select_html = s.render(field % name, val, local_attrs)
        return select_html


class BetterDecimalField(models.DecimalField):
    def __init__(self, verbose_name=None, name=None, max_digits=None,
                 decimal_places=None, suffix=None, **kwargs):

        self.max_digits, self.decimal_places, self.suffix = max_digits, decimal_places, suffix
        super(models.DecimalField, self).__init__(verbose_name, name, **kwargs)


class BetterPositiveIntegerField(models.PositiveIntegerField):
    def __init__(self, suffix=None, **kwargs):

        self.suffix = suffix
        super(models.PositiveIntegerField, self).__init__(**kwargs)