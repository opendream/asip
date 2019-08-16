from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from taxonomy.models import *



class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        fields = (
            'id', 'permalink', 'title', 'parent', 'priority'
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

############## New For 2018 ######################
class ProgramTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProgramType, ProgramTypeAdmin)

class TypeOfOfficeAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfOffice, TypeOfOfficeAdmin)

class TypeOfFocusSectorAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfFocusSector, TypeOfFocusSectorAdmin)

class TypeOfFocusIndustryAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfFocusIndustry, TypeOfFocusIndustryAdmin)

class TypeOfStageOfParticipantAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfStageOfParticipant, TypeOfStageOfParticipantAdmin)

class TypeOfInvestmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfInvestment, TypeOfInvestmentAdmin)

class TypeOfInvestmentStageAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfInvestmentStage, TypeOfInvestmentStageAdmin)

class TypeOfFundingAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfFunding, TypeOfFundingAdmin)

class TypeOfBatchAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfBatch, TypeOfBatchAdmin)

class TypeOfAssistantshipAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfAssistantship, TypeOfAssistantshipAdmin)

class TypeOfAttachmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(TypeOfAttachment, TypeOfAttachmentAdmin)

class JobRoleAdmin(MPTTModelAdmin):
    pass
admin.site.register(JobRole, JobRoleAdmin)

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)