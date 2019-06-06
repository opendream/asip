from django.contrib import admin

# Register your models here.
from cms.models import News
from cms.models import Event

class NewsAdmin(admin.ModelAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(News, NewsAdmin)
admin.site.register(Event, EventAdmin)
