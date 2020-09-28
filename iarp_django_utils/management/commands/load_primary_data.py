from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from iarp_utils.benchmarks import Benchmark


class Command(BaseCommand):
    help = "loaddata's various primary fixtures"

    def handle(self, *args, **kwargs):
        for app in settings.INSTALLED_APPS:
            app_init_data = __import__(app)
            models = None
            try:
                models = app_init_data.__fixture_load_models__
            except AttributeError:
                pass

            if not models:
                continue

            try:
                file_prefix = app_init_data.__fixture_prefix__
            except AttributeError:
                file_prefix = app

            for model in models:
                cargs = [
                    f'{file_prefix}_{model}.json',
                    '--app', app,
                ]
                with Benchmark(f'Loading {app}.{model}'):
                    try:
                        call_command('loaddata', *cargs)
                    except CommandError as e:
                        print(e)
