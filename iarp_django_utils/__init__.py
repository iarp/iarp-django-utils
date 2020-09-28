import os

from django.conf import settings

from iarp_utils import configuration


default_app_config = 'iarp_django_utils.apps.IarpDjangoUtilsConfig'

UTILS_CONFIG_FILE = os.path.join(settings.BASE_DIR, 'IARPUTILS.json')
CONFIG = configuration.load(UTILS_CONFIG_FILE)


def save_config(config):
    configuration.save(config=config, file_location=UTILS_CONFIG_FILE)
