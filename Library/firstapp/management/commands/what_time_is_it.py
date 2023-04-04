from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.utils import timezone


class Command(BaseCommand):
    # help = 'Display current time'
    # def handle(self, *args, **kwargs):
    #     time = timezone.now().strftime('%x')
    #     self.stdout.write("its now %s" % time)
    #     print(time)

    help = 'create random users'
    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='help indicate the number of users to be created')

    def handle(self, *args, **kwargs):
        # print(kwargs)
        total = kwargs['total']
        for i in range(total):
            User.objects.create_user(username=get_random_string(), email='', password='123')