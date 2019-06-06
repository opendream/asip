from django.contrib import admin
from django.contrib.auth.models import Group
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from account.models import User
from tastypie.models import ApiKey, ApiAccess
from notifications.models import Notification
from social_auth.models import *
from party.models import Portfolio
from relation.models import *


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'homepage_url', 'facebook_url', 'date_joined'
        )

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

    list_filter = ('interests', 'user_roles', 'is_active')


admin.site.register(User, UserAdmin)

# Hide admin model from webmaster
#admin.site.unregister(ApiKey)
#admin.site.unregister(Notification)
#admin.site.unregister(Association)
#admin.site.unregister(Nonce)
#admin.site.unregister(UserSocialAuth)
#admin.site.unregister(Group)
admin.site.register(Portfolio)
admin.site.register(PartyPartnerParty)
admin.site.register(PartySupportParty)
admin.site.register(PartyInvestParty)
admin.site.register(PartyFollowParty)
admin.site.register(PartyContactParty)
admin.site.register(PartyTestifyParty)
admin.site.register(UserExperienceOrganization)
admin.site.register(PartyReceivedFundingParty)
admin.site.register(PartyReceivedInvestingParty)
admin.site.register(PartyInviteTestifyParty)
admin.site.register(PartyLove)
