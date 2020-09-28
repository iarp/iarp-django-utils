import os

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "dumpdata's various primary fixtures"

    def handle(self, *args, **kwargs):
        for app in apps.get_app_configs():
            app_init_data = __import__(app.name)
            models = None
            try:
                models = app_init_data.__fixture_dump_models__
            except AttributeError:
                pass

            if not models:
                continue

            try:
                file_prefix = app_init_data.__fixture_prefix__
            except AttributeError:
                file_prefix = app

            fixture_dir = os.path.join(app, 'fixtures')
            if not os.path.isdir(fixture_dir):
                os.mkdir(fixture_dir)

            for model in models:
                print(f'Dumping {app}.{model} to {fixture_dir}\\{file_prefix}_{model}.json')
                cargs = [
                    '.'.join([app, model]),
                    '--output', os.path.join(fixture_dir, f'{file_prefix}_{model}.json'),
                    '--indent', '4'
                ]
                call_command('dumpdata', *cargs)
