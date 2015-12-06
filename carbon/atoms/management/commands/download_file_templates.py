import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from carbon.utils.template import get_page_templates, get_page_templates_raw

from ...models import Template


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):

        print "TODO..."
        