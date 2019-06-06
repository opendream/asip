from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from taxonomy.models import *



class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        fields = (
            'id', 'permalink', 'title_th', 'title_en', 'parent', 'priority'
        )

class TopicAdmin(MPTTModelAdmin, ImportExportModelAdmin):
    resource_class = TopicResource
admin.site.register(Topic, TopicAdmin)

class TypeOfNeedAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfNeed, TypeOfNeedAdmin)

class TypeOfSupportAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfSupport, TypeOfSupportAdmin)

class InterestAdmin(admin.ModelAdmin):
    pass
admin.site.register(Interest, InterestAdmin)

class OrganizationRoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrganizationRole, OrganizationRoleAdmin)

class OrganizationProductLaunchAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrganizationProductLaunch, OrganizationProductLaunchAdmin)

class OrganizationFundingAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrganizationFunding, OrganizationFundingAdmin)

class OrganizationGrowthStageAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrganizationGrowthStage, OrganizationGrowthStageAdmin)

class UserRoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserRole, UserRoleAdmin)

class CountryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Country, CountryAdmin)

class OrganizationTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrganizationType, OrganizationTypeAdmin)

class InvestorTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(InvestorType, InvestorTypeAdmin)

class ArticleCategoryAdmin(MPTTModelAdmin):
    pass
admin.site.register(ArticleCategory, ArticleCategoryAdmin)