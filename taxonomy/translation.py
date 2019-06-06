from modeltranslation.translator import translator, TranslationOptions
from taxonomy.models import BaseTaxonomy, Topic


class BaseTaxonomyTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'description')

for cls in BaseTaxonomy.__subclasses__():
    translator.register(cls, BaseTaxonomyTranslationOptions)
