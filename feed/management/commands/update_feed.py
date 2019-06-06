from django.core.management import BaseCommand
from feed import FeedResource

class Command(BaseCommand):

    def handle(self, *args, **options):
        feed_resource = FeedResource()
        feed_resource.update_feed()

