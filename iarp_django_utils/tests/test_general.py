from iarp_django_utils.app_settings import app_settings

from .base_test_classes import BaseTestClassMethods


class GeneralTests(BaseTestClassMethods):
    def test_app_settings_defaults(self):
        self.assertTrue(app_settings.SETTINGS_BLANK_HOSTNAME_IS_DEFAULT)
        self.assertTrue(app_settings.SETTINGS_USE_HOSTNAME_SEPARATION)
