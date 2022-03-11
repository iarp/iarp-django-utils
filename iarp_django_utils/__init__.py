import os

import django
from django.conf import settings

from iarp_utils import configuration

if django.VERSION < (4, 0):
    default_app_config = "iarp_django_utils.apps.IarpDjangoUtilsConfig"

UTILS_CONFIG_FILE = os.path.join(settings.BASE_DIR, "IARPUTILS.json")
CONFIG = configuration.load(UTILS_CONFIG_FILE)


def save_config(config):
    configuration.save(config=config, file_location=UTILS_CONFIG_FILE)
