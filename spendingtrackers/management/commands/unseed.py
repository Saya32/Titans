from django.core.management.base import BaseCommand
from spendingtrackers.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter().delete()