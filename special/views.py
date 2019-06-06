from django.shortcuts import render, get_object_or_404
from account.models import User
from common.constants import STATUS_PUBLISHED
from forum.models import Forum
from organization.models import Organization
from special.models import Page
from taxonomy.models import OrganizationRole


def page_detail(request, permalink):

    page = get_object_or_404(Page, permalink__iexact=permalink)

    forums = []
    organizations = []
    people = []

    if page.special:

        if not request.session.get('has_session'):
            request.session['has_session'] = True
            request.session['special'] = page.special.permalink
            request.session.save()

        forums = Forum.objects.filter(parent=page.special)

        for role in OrganizationRole.objects.all():

            items = Organization.objects.filter(
                status=STATUS_PUBLISHED,
                organization_primary_role=role,
                specials=page.special
            )
            if items:
                organizations.append((role, items))

        people = User.objects.filter(is_active=True, specials=page.special).exclude(username='admin')


    return render(request, 'page/%s.html' % page.permalink, {
        'page': page,
        'forums': forums,
        'organizations': organizations,
        'people': people
    })
