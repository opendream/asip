import json
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields

from django.contrib import admin
from organization.models import Organization


class OrganizationResource(resources.ModelResource):
    phone_number_of_organizations_headquarters = fields.Field()
    total_follower = fields.Field()
    total_following = fields.Field()
    total_love = fields.Field()
    total_views = fields.Field()

    last_owner_visit_date = fields.Field()
    last_visit_date = fields.Field()

    class Meta:
        model = Organization
        fields = (
            # information
            'id', 'name', 'permalink', 'name_of_representative', 'location_of_organizations_headquarters', 'phone_number_of_organizations_headquarters',
            # taxonomy
            'kind', 'product_launch__title', 'funding__title', 'request_funding__title',
            # statistic
            'total_follower', 'total_following', 'total_love', 'total_views',
            'created', 'last_visit_date',
            # contact
            'email_of_contact_person', 'created_by__email',
            # link
            'homepage_url', 'facebook_url',
        )
        export_order = fields

    def dehydrate_phone_number_of_organizations_headquarters(self, obj):
       return ', '.join([item['phone_number'] for item in obj.phone_number_of_organizations_headquarters])

    def dehydrate_total_follower(self, obj):
        return obj.total_follower

    def dehydrate_total_following(self, obj):
        return obj.total_following

    def dehydrate_total_love(self, obj):
        return obj.total_love

    def dehydrate_total_views(self, obj):
        return obj.total_views

    def dehydrate_last_visit_date(self, obj):
        return obj.last_visit_date



class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource

    list_filter = ('type_of_organization', 'organization_primary_role', 'organization_roles', 'organization_types', 'investor_types', 'status', 'is_deleted')

    def get_queryset(self, request):
        qs = Organization.objects.all()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Organization, OrganizationAdmin)


# Organization Types
class OrganizationOrganizationTypesResource(resources.ModelResource):
    class Meta:
        model = Organization.organization_types.through
        fields = (
            'organization__id', 'organization__permalink', 'organization__name',
            'organizationtype__id', 'organizationtype__permalink', 'organizationtype__title',
        )
        export_order = fields


class OrganizationOrganizationTypesAdmin(ImportExportModelAdmin):
    resource_class = OrganizationOrganizationTypesResource

admin.site.register(Organization.organization_types.through, OrganizationOrganizationTypesAdmin)


# Investor Types
class OrganizationInvestorTypesResource(resources.ModelResource):
    class Meta:
        model = Organization.investor_types.through
        fields = (
            'organization__id', 'organization__permalink', 'organization__name',
            'investortype__id', 'investortype__permalink', 'investortype__title',
        )
        export_order = fields


class OrganizationInvestorTypesAdmin(ImportExportModelAdmin):
    resource_class = OrganizationInvestorTypesResource

admin.site.register(Organization.investor_types.through, OrganizationInvestorTypesAdmin)


# Topics
class OrganizationTopicsResource(resources.ModelResource):
    class Meta:
        model = Organization.topics.through
        fields = (
            'organization__id', 'organization__permalink', 'organization__name',
            'topic__id', 'topic__permalink', 'topic__title',
        )
        export_order = fields


class OrganizationTopicsAdmin(ImportExportModelAdmin):
    resource_class = OrganizationTopicsResource

admin.site.register(Organization.topics.through, OrganizationTopicsAdmin)


# Type of Needs
class OrganizationTypeOfNeedsResource(resources.ModelResource):
    class Meta:
        model = Organization.type_of_needs.through
        fields = (
            'organization__id', 'organization__permalink', 'organization__name',
            'typeofneed__id', 'typeofneed__permalink', 'typeofneed__title',
        )
        export_order = fields


class OrganizationTypeOfNeedsAdmin(ImportExportModelAdmin):
    resource_class = OrganizationTypeOfNeedsResource

admin.site.register(Organization.type_of_needs.through, OrganizationTypeOfNeedsAdmin)


# Type of Supports
class OrganizationTypeOfSupportsResource(resources.ModelResource):
    class Meta:
        model = Organization.type_of_supports.through
        fields = (
            'organization__id', 'organization__permalink', 'organization__name',
            'typeofsupport__id', 'typeofsupport__permalink', 'typeofsupport__title',
        )
        export_order = fields


class OrganizationTypeOfSupportsAdmin(ImportExportModelAdmin):
    resource_class = OrganizationTypeOfSupportsResource

admin.site.register(Organization.type_of_supports.through, OrganizationTypeOfSupportsAdmin)
