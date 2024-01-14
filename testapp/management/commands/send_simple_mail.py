from django.conf import settings
from django.core.management import BaseCommand

from testapp import utils


class Command(BaseCommand):

    def handle(self, *args, **options):
        utils.send_simple_mail(
            settings.FROM_EMAIL,
            ['johndoe@example.com', 'Jane Doe <janedoe@example.com>'],
            ['johnjr@example.com', 'Jane Jr <janejr@example.com>']
        )
