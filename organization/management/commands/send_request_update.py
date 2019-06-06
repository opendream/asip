from optparse import make_option
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from account.models import User
from common.functions import PermanentTokenGenerator


class Command(BaseCommand):

    help = 'Send Request Update to Organization Administrators'

    option_list = BaseCommand.option_list + (
        make_option('--limit',
            action='store',
            dest='limit',
            default=0,
            help='limit'),
        )

    def handle(self, *args, **options):

        token_generator = PermanentTokenGenerator()

        success_num = 0

        limit = int(options.get('limit', 0))

        for user in User.objects.filter(is_active=True).order_by('id'):
            if user.created_by.all().count() or user.admins.all().count():

                organization_list = set(user.created_by.all()) | set(user.admins.all())

                context = {
                    'organization_list': organization_list,
                    'site_url': settings.SITE_URL,
                    'domain': settings.SITE_NAME,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': token_generator.make_token(user),
                }

                subject = loader.render_to_string('organization/send_request_update_subject.txt', context)
                message = loader.render_to_string('organization/send_request_update.txt', context)
                html_message = loader.render_to_string('organization/send_request_update.html', context)
                from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(subject, message, from_email, [user.email], html_message=html_message)

                success_num += 1

                print 'send email update %s to %s(%s)' % ([o.name for o in organization_list], user, user.id)

                if limit and success_num >= limit:
                    break