from haystack import indexes
from relation.models import OrganizationHasPeople, PartyPartnerParty, PartySupportParty, PartyInvestParty, UserExperienceOrganization, PartyReceivedFundingParty, PartyReceivedInvestingParty, OrganizationParticipate


class BaseRelationIndex(indexes.ModelSearchIndex):

    content_type = indexes.CharField(default='Relation')

    src = indexes.CharField(indexed=True, stored=True)
    src_status = indexes.IntegerField(indexed=True, stored=True)
    src_is_mockup = indexes.BooleanField(indexed=True, stored=True)

    dst = indexes.CharField(indexed=True, stored=True)
    dst_status = indexes.IntegerField(indexed=True, stored=True)
    dst_is_mockup = indexes.BooleanField(indexed=True, stored=True)

    # dst_is_mockup = indexes.BooleanField(indexed=True, stored=True)

    status = indexes.IntegerField(indexed=True, stored=True)

    text = indexes.CharField(document=True, use_template=True, template_name='search/indexes/relation/default_text.txt')

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter()

    def prepare_src(self, object):
        return ('%s' % object.src).lower()

    def prepare_src_status(self, object):
        inst = object.src and object.src.get_inst()
        return (inst and inst.get_status()) or 0

    def prepare_dst(self, object):
        return ('%s' % object.dst).lower()

    def prepare_dst_status(self, object):
        inst = object.dst and object.dst.get_inst()
        return (inst and inst.get_status()) or 0

    def prepare_src_is_mockup(self, object):
        inst = object.src and object.src.get_inst()
        return inst and hasattr(inst, 'is_mockup') and inst.is_mockup

    def prepare_dst_is_mockup(self, object):
        inst = object.dst and object.dst.get_inst()
        return inst and hasattr(inst, 'is_mockup') and inst.is_mockup

class OrganizationHasPeopleIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='OrganizationHasPeople')
    class Meta:
        model = OrganizationHasPeople

class PartyPartnerPartyIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='PartyPartnerParty')
    class Meta:
        model = PartyPartnerParty

class PartySupportPartyIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='PartySupportParty')
    class Meta:
        model = PartySupportParty

class PartyInvestPartyIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='PartyInvestParty')
    class Meta:
        model = PartyInvestParty

class UserExperienceOrganizationIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='UserExperienceOrganization')
    class Meta:
        model = UserExperienceOrganization

class PartyReceivedFundingPartyIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='PartyReceivedFundingParty')
    class Meta:
        model = PartyReceivedFundingParty

class PartyReceivedInvestingPartyIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='PartyReceivedInvestingParty')
    class Meta:
        model = PartyReceivedInvestingParty

class OrganizationParticipateIndex(BaseRelationIndex, indexes.Indexable):
    verb = indexes.CharField(default='OrganizationParticipate')
    class Meta:
        model = OrganizationParticipate

