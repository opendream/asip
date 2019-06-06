from django.core.management import BaseCommand
from django.http import HttpRequest
from organization.models import Organization
from organization.views import organization_create


class Command(BaseCommand):

    help = 'Rebuild Organization Point'

    def handle(self, *args, **options):

        for organization in Organization.objects.filter():
            request = HttpRequest()
            request.user = organization.created_by
            request.logged_in_party = organization.created_by
            organization_create(request, organization.type_of_organization, organization, True)
            print 'Build point complete: %s' % organization.get_display_name()