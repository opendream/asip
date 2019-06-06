import os
from urlparse import urlparse
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Max, Min
from django.shortcuts import get_object_or_404, render, redirect
from django.template import TemplateDoesNotExist
from django.utils import timezone
from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.utils.dates import MONTHS
from account.functions import user_can_edit_check

from cms.forms import NewsForm, EventForm
from cms.models import News, Event
from common.functions import instance_set_permalink, get_success_message, get_cms_success_message
from django.template.defaultfilters import truncatechars
from django.utils.html import strip_tags
from party.models import Party
from relation.models import CmsHasParty
from taxonomy.models import ArticleCategory


@login_required
def news_create(request, article_category=None, instance=None):

    # Config for reuse
    ModelClass = News
    instance = instance or ModelClass()

    form = NewsForm(instance, ModelClass, request.user, request.POST)
    is_new = form.is_new()

    if article_category:
        try:
            article_category = ArticleCategory.objects.filter(level=0, permalink=article_category).first()
        except ArticleCategory.DoesNotExist:
            raise Http404()

    if instance.id:
        article_category = instance.categories.filter(level=0).first()

    if request.method == 'POST':

        form = NewsForm(instance, ModelClass, request.user, request.POST)

        is_new = form.is_new()

        if form.is_valid():

            # Relation
            if not instance.created_by_id:
                instance.created_by = request.user

            if not instance.party_created_by_id:
                instance.party_created_by = request.logged_in_party

            instance.permalink = form.cleaned_data['permalink']
            instance.title = form.cleaned_data['title']

            if form.cleaned_data['summary'] == '':
                summary = strip_tags(form.cleaned_data['description'])
                instance.summary = truncatechars(summary, 240)
            else:
                instance.summary = form.cleaned_data['summary']

            instance.description = form.cleaned_data['description']
            #instance.organization = form.cleaned_data['organization']
            instance.article_category = form.cleaned_data['article_category']
            instance.homepage_url = form.cleaned_data['homepage_url']

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data['image'])


            instance_files = instance._meta.get_field('files')
            if instance_files:
                instance_files.save_form_data(instance, form.cleaned_data['files'])

            instance.is_promoted = form.cleaned_data['is_promoted']
            instance.tags = form.cleaned_data['tags']

            instance.changed = timezone.now()
            instance.save()

            instance.topics.clear()
            for topic in form.cleaned_data['topics']:
                instance.topics.add(topic)

            instance.categories.clear()
            for category in form.cleaned_data['categories']:
                instance.categories.add(category)

            CmsHasParty.objects.filter(src=instance).exclude(dst=form.cleaned_data['in_the_news']).delete()
            for party in form.cleaned_data['in_the_news']:
                CmsHasParty.objects.get_or_create(src=instance, dst=party)

            message_success = get_cms_success_message(instance, is_new, [])
            messages.success(request, message_success)
            return redirect('article_edit', instance.id)
        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')

    else:
        if not instance.id:
            if request.user.is_staff:
                instance.is_promoted = True
            else:
                instance.is_promoted = False

        initial = {
            'permalink': instance.permalink,
            'title': instance.title,
            'image': instance.image,
            #'organization': instance.organization,
            'summary': instance.summary,
            'description': instance.description,
            'homepage_url': instance.homepage_url,
            'article_category': instance.article_category,
            'is_promoted': instance.is_promoted,
            'tags': instance.tags,
            'files': instance.files,

        }
        if instance.id:
            initial['topics'] = instance.topics.all()
            initial['categories'] = instance.categories.all()
            initial['in_the_news'] = Party.objects.filter(cms_has_party_dst__src=instance).distinct()


        else:
            initial['article_category'] = request.GET.get('article_category') # deprecate
            if article_category:
                initial['categories'] = [article_category]

        form = NewsForm(instance, ModelClass, request.user, initial=initial)
    return render(request, 'cms/news/form.html', {
        'form': form,
        'article_category': article_category,
        'show_category_field': article_category and article_category.get_children().count(),
        'is_staff': request.user.is_staff
    })

def news_edit(request, news_id=None):

    news = get_object_or_404(News, id=news_id)

    user_can_edit_check(request, news)


    return news_create(request, instance=news)


def news_detail(request, news_permalink, news_id):

    instance = get_object_or_404(News, id=news_id)

    return render(request, 'cms/news/detail.html',{
        'news_id': news_id,
        'article_category': 'news',
        'article_category_name': 'News',
        'instance': instance
    })

def article_detail(request, article_category, news_permalink, news_id):
    instance = get_object_or_404(News, id=news_id)

    if article_category == 'knowledge-tools':
        article_category_name = 'Knowledge & Tools'
    else:
        article_category_name = article_category.title()
    return render(request, 'cms/news/detail.html',{
        'news_id': news_id,
        'article_category': article_category,
        'article_category_name': article_category_name,
        'instance': instance
    })

def article_list(request, article_category='news'):


    article_category = get_object_or_404(ArticleCategory, permalink=article_category)

    year_min = News.objects.all().aggregate(Min('created'))['created__min']
    year_min = (year_min and year_min.year) or datetime.date.today().year

    year_list = range(year_min, datetime.date.today().year + 1)

    year_list = [{'title': year, 'permalink': year} for year in year_list]
    month_list = [{'permalink': permalink, 'title': title} for permalink, title in MONTHS.iteritems()]

    context = {
        'year_list': year_list,
        'show_year_filter': len(year_list) > 1,
        'month_list': month_list,

        'item_template': '<div ng-include="\'template_party_news.html\'"></div>',

        'article_category': article_category,
        'article_category_name': article_category.title # deprecate
    }

    try:
        return render(request, 'cms/news/%s_list.html' % article_category.permalink, context)
    except TemplateDoesNotExist:
        return render(request, 'cms/news/list.html', context)


#==================================== Event views =========================
@login_required
def event_create(request, instance=None):

    # Config for reuse
    ModelClass = Event
    instance = instance or ModelClass()

    form = EventForm(instance, ModelClass, request.user, request.POST)
    is_new = form.is_new()
    if request.method == 'POST':

        form = EventForm(instance, ModelClass, request.user, request.POST)

        is_new = form.is_new()
        if form.is_valid():

            # Relation
            if not instance.created_by_id:
                instance.created_by = request.user

            if not instance.party_created_by_id:
                instance.party_created_by = request.logged_in_party

            # Common fields
            instance.permalink = form.cleaned_data['permalink']
            instance.title = form.cleaned_data['title']

            if form.cleaned_data['summary'] == '':
                summary = strip_tags(form.cleaned_data['description'])
                instance.summary = truncatechars(summary, 240)
            else:
                instance.summary = form.cleaned_data['summary']

            instance.description = form.cleaned_data['description']
            #instance.organization = form.cleaned_data['organization']
            instance.changed = timezone.now()

            instance_image = instance._meta.get_field('image')
            if instance_image:
                instance_image.save_form_data(instance, form.cleaned_data['image'])
            # Event fields
            instance.location = form.cleaned_data['location']
            instance.start_date = form.cleaned_data['start_date']
            instance.end_date = form.cleaned_data['end_date']

            if instance.end_date is None:
                instance.end_date = form.cleaned_data['start_date']

            instance.time = form.cleaned_data['time']
            instance.phone = form.cleaned_data['phone']
            instance.email = form.cleaned_data['email']
            instance.facebook_url = form.cleaned_data['facebook_url']
            instance.twitter_url = form.cleaned_data['twitter_url']
            instance.homepage_url = form.cleaned_data['homepage_url']
            instance.is_promoted = form.cleaned_data['is_promoted']
            instance.tags = form.cleaned_data['tags']


            instance.save()
            instance.topics.clear()
            instance.topics.clear()
            for topic in form.cleaned_data['topics']:
                instance.topics.add(topic)

            CmsHasParty.objects.filter(src=instance).exclude(dst=form.cleaned_data['in_the_news']).delete()
            for party in form.cleaned_data['in_the_news']:
                CmsHasParty.objects.get_or_create(src=instance, dst=party)

            message_success = get_success_message(instance, is_new, [])
            messages.success(request, message_success)
            return redirect('event_edit', instance.id)

        else:
            messages.error(request, 'Your submission error. Please, check in error fields.')
    else:

        if not instance.id:
            if request.user.is_staff:
                instance.is_promoted = True
            else:
                instance.is_promoted = False

        initial = {
            'permalink': instance.permalink,
            'title': instance.title,
            'image': instance.image,
            #'organization': instance.organization,
            'summary': instance.summary,
            'description': instance.description,
            'location': instance.location,
            'start_date': instance.start_date,
            'end_date': instance.end_date,
            'time': instance.time,
            'phone': instance.phone,
            'email': instance.email,
            'facebook_url': instance.facebook_url,
            'twitter_url': instance.twitter_url,
            'homepage_url': instance.homepage_url,
            'is_promoted': instance.is_promoted,
            'tags': instance.tags
        }
        if instance.id:
            initial['topics'] = instance.topics.all()
            initial['in_the_news'] = Party.objects.filter(cms_has_party_dst__src=instance).distinct()

        form = EventForm(instance, ModelClass, request.user, initial=initial)
    return render(request, 'cms/event/form.html', {'form': form, 'is_staff': request.user.is_staff})

def event_edit(request, event_id=None):

    event = get_object_or_404(Event, id=event_id)

    # Check permission
    user_can_edit_check(request, event)

    return event_create(request, event)


def event_detail(request, event_permalink, event_id):
    instance = get_object_or_404(Event, id=event_id)
    return render(request, 'cms/event/detail.html',{
        'event_id': event_id,
        'instance': instance
    })

def event_list(request):

    year_max = Event.objects.all().aggregate(Max('end_date'))['end_date__max']
    year_max = (year_max and year_max.year) or datetime.date.today().year

    year_list = range(datetime.date.today().year, year_max + 1)

    year_list = [{'title': year, 'permalink': year} for year in year_list]
    month_list = [{'permalink': permalink, 'title': title} for permalink, title in MONTHS.iteritems()]

    return render(request, 'cms/event/list.html', {
        'year_list': year_list,
        'show_year_filter': len(year_list) > 1,
        'month_list': month_list
    })

def event_past_list(request):

    return render(request, 'cms/event/past_list.html')

def updates_landing(request):
    return redirect('news_list')
