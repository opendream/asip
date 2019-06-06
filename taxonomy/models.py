from django.core.urlresolvers import reverse
from django.db import models
from ckeditor.fields import RichTextField

from mptt.models import MPTTModel, TreeForeignKey
from common.functions import camelcase_to_underscore
from common.models import CommonTrashModel, AbstractPermalink


class BaseTaxonomy(CommonTrashModel, AbstractPermalink):

    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    priority = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-priority', 'id']

    def __unicode__(self):
        return self.title


    def get_absolute_url(self):
        if not self.permalink:
            return ''

        return reverse('%s_detail' % camelcase_to_underscore(self.__class__.__name__), args=[self.permalink])

# ======================================
# Organization
# ======================================

class Topic(MPTTModel, BaseTaxonomy):

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['-priority', 'title']


class TypeOfNeed(BaseTaxonomy):
    pass


class TypeOfSupport(BaseTaxonomy):
    pass

class OrganizationRole(BaseTaxonomy):
    pass

class OrganizationType(BaseTaxonomy):
    pass

class InvestorType(BaseTaxonomy):
    pass

class OrganizationProductLaunch(BaseTaxonomy):
    pass

class OrganizationFunding(BaseTaxonomy):
    pass

class OrganizationGrowthStage(BaseTaxonomy):
    pass

# ======================================
# People
# ======================================

class Interest(BaseTaxonomy):
    pass


class UserRole(BaseTaxonomy):
    pass


# ======================================
# Both
# ======================================

class Country(BaseTaxonomy):
    pass

# ======================================
# CMS
# ======================================
class ArticleCategory(MPTTModel, BaseTaxonomy):

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['-priority', 'title']