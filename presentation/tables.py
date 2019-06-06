from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from django_tables2.utils import A, AttributeDict
from common.constants import STATUS_CHOICES
from common.functions import instance_get_thumbnail

import django_tables2 as tables


# Field col
from organization.models import Organization


class SafeLinkColumn(tables.LinkColumn):
    def render_link(self, uri, text, attrs=None):

        attrs = AttributeDict(attrs if attrs is not None else
                              self.attrs.get('a', {}))
        attrs['href'] = uri
        html = '<a {attrs}>{text}</a>'.format(
            attrs=attrs.as_html(),
            text=text.encode('utf-8')
        )
        return mark_safe(html)


class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe('<div class="small-logo thumbnail"><span><img src="%s" /></span></div>' % instance_get_thumbnail(bypass_image=value, size='80x80', crop=None))

class StatusColumn(tables.Column):
    def render(self, value):
        try:
            return dict(STATUS_CHOICES)[value]
        except KeyError:
            return value

class DateColumn(tables.Column):
    def render(self, value):
        return value.strftime('%B %d, %Y')

class MultipleColum(tables.Column):
    def render(self, value, record, bound_column):
        return ', '.join([ v.__unicode__() for v in getattr(record, bound_column.name).all()])

class OrderColum(tables.Column):
    def render(self, value):
        return mark_safe('<input type="text" value="%s" name=""/> ' % value)





# Tables

class SortableTable(tables.Table):
    priority = tables.Column(verbose_name=_('Priority'))
    id = tables.Column(visible=False)
    promote = tables.Column(verbose_name=_('Checkout'))

    def render_priority(self, value, bound_row, record):
        return mark_safe('<input type="text" value="%s" name="priority-id-%s" readonly /> ' % (value, bound_row['id']))

    def render_promote(self, value, bound_row, record):
        return mark_safe('<input type="checkbox" value="%s" name="promote-id-%s" id="promote-id-%s" /><label for="promote-id-%s"></label> ' % (value, bound_row['id'], bound_row['id'], bound_row['id']))


class OrganizationTable(tables.Table):
    image = ImageColumn()
    name = SafeLinkColumn('organization_edit', args=[A('id')], verbose_name=_('Name'))
    created_by = SafeLinkColumn('people_edit', args=[A('id')], accessor='created_by.get_display_name', verbose_name=_('Created by'))
    status = StatusColumn(verbose_name=_('Status'))
    created = DateColumn(verbose_name=_('Created'))
    specials = MultipleColum(accessor="specials.all.0", empty_values=())


    class Meta:
        model = Organization
        fields = ('image', 'name', 'created_by', 'status', 'created', 'specials')

    # def render_specials(self, value):
    #     print value
    #     return ', '.join([v.__unicode__() for v in value.all()])

class SortableOrganizationTable(OrganizationTable, SortableTable):

    class Meta:
        fields = ('id', 'priority', 'image',  'name', 'created_by', 'status', 'created', 'specials')


class PeopleTable(tables.Table):
    image = ImageColumn()
    name = SafeLinkColumn('people_edit', args=[A('id')], accessor='get_display_name', verbose_name=_('Name'))
    is_active = StatusColumn(verbose_name=_('Active'))
    date_joined = DateColumn(verbose_name=_('Date joined'))

    class Meta:
        model = Organization
        fields = ('image', 'name', 'is_active', 'date_joined')

class SortablePeopleTable(PeopleTable, SortableTable):

    class Meta:
        fields = ('id', 'priority', 'image', 'name', 'is_active', 'date_joined')
