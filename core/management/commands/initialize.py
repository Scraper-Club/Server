from django.core.management.base import BaseCommand, CommandError
from core.models import TokenRuleChainModel

class Command(BaseCommand):
    help = 'Initializes the application'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            pass
        except TokenRuleChainModel.DoesNotExist:
            pass