from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.utils import timezone


class Command(BaseCommand):
    help = 'Display current time'
    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%x')
        self.stdout.write("its now %s" % time)
