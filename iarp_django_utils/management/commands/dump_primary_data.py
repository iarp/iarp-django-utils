import os

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "dumpdata's various primary fixtures"

    def handle(self, *args, **kwargs):
        for app in apps.get_app_configs():
            app_name = app.name
            app_init_data = __import__(app_name)

            try:
                models = app_init_data.__fixture_dump_models__
            except AttributeError:
                models = None

            if not models:
                continue

            try:
                file_prefix = app_init_data.__fixture_prefix__
            except AttributeError:
                file_prefix = app_name

            fixture_dir = os.path.join(app_name, "fixtures")
            os.makedirs(fixture_dir, exist_ok=True)

            for model in models:
                print(f"Dumping {app_name}.{model} to {fixture_dir}\\{file_prefix}_{model}.json")
                cargs = [
                    ".".join([app_name, model]),
                    "--output",
                    os.path.join(fixture_dir, f"{file_prefix}_{model}.json"),
                    "--indent",
                    "4",
                ]
                call_command("dumpdata", *cargs)
