from django.conf.urls import patterns, include
from tastypie.api import Api

from api.resources import *


v1_api = Api(api_name='v1')

# Taxonomy
v1_api.register(TopicResource())
v1_api.register(ArticleCategoryItemResource())
v1_api.register(TypeOfNeedResource())
v1_api.register(TypeOfSupportResource())
v1_api.register(InterestResource())
v1_api.register(UserRoleResource())
v1_api.register(CountryResource())
v1_api.register(OrganizationTypeResource())
v1_api.register(InvestorTypeResource())
v1_api.register(OrganizationProductLaunchResource())
v1_api.register(OrganizationFundingResource())
v1_api.register(OrganizationGrowthStageResource())

############## New For 2018 ######################
v1_api.register(ProgramTypeResource())
v1_api.register(TypeOfOfficeResource())
v1_api.register(TypeOfFocusSectorResource())
v1_api.register(TypeOfFocusIndustryResource())
v1_api.register(TypeOfStageOfParticipantResource())
v1_api.register(TypeOfInvestmentResource())
v1_api.register(TypeOfInvestmentStageResource())
v1_api.register(TypeOfFundingResource())
v1_api.register(TypeOfBatchResource())
v1_api.register(TypeOfFinancialSourceResource())
v1_api.register(TypeOfAssistantshipResource())
v1_api.register(TypeOfAttachmentResource())
v1_api.register(JobRoleResource())
v1_api.register(LocationResource())

# Account
v1_api.register(UserResource())
v1_api.register(PartyLiteResource())
v1_api.register(PartyResource())

# Organization
v1_api.register(OrganizationResource())
v1_api.register(ProgramResource())
v1_api.register(JobResource())
v1_api.register(UserApplyJobResource())
v1_api.register(OrganizationJobsResource())
v1_api.register(SkillResource())
v1_api.register(JobTagResource())
v1_api.register(OrganizationStaffResource())


# Relation
v1_api.register(OrganizationHasPeopleResource())
v1_api.register(PartySupportPartyResource())
v1_api.register(PartyInvestPartyResource())
v1_api.register(PartyPartnerPartyResource())
v1_api.register(PartyFollowPartyResource())
v1_api.register(PartyContactPartyResource())
v1_api.register(PartyTestifyPartyResource())
v1_api.register(OrganizationParticipateResource())
v1_api.register(PartyInviteTestifyPartyResource())
v1_api.register(PartyReceivedFundingPartyResource())
v1_api.register(PartyReceivedInvestingPartyResource())
v1_api.register(PartyLoveResource())
v1_api.register(UserExperienceOrganizationResource())

# Party
v1_api.register(PortfolioResource())
v1_api.register(PartyFollowingResource())

#CMS
v1_api.register(NewsResource())
v1_api.register(EventResource())
v1_api.register(NewsTagResource())
v1_api.register(EventTagResource())


# Notification
v1_api.register(VerbResource())
v1_api.register(NotificationResource())
v1_api.register(RequestResource())

v1_api.register(HappeningResource())

v1_api.register(SearchResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)),
)