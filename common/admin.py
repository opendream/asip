from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields

from common.models import StatisitcAccess


class StatisitcAccessResource(resources.ModelResource):

    content_object = fields.Field(attribute='content_object')

    class Meta:
        model = StatisitcAccess
        fields = (
            'content_type__name', 'object_id', 'content_object', 'created', 'ip_address',
        )
        export_order = fields

class StatisitcAccessAdmin(ImportExportModelAdmin):
    resource_class = StatisitcAccessResource

    list_filter = ('content_type', )


admin.site.register(StatisitcAccess, StatisitcAccessAdmin)

