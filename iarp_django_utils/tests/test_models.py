import socket

from django.test.utils import override_settings

from .base_test_classes import BaseTestClassMethods
from iarp_django_utils.models import BaseSetting


class GeneralTests(BaseTestClassMethods):
    def test_basesetting_gethostname_resolution(self):
        expected_hostname = socket.gethostname().lower().replace('.', '')
        settings_hostname = BaseSetting._get_hostname(system_specific=True)
        self.assertEqual(expected_hostname, settings_hostname)

    def test_basesetting_gethostname_systemspecific_false(self):
        expected_hostname = ''
        settings_hostname = BaseSetting._get_hostname(system_specific=False)
        self.assertEqual(expected_hostname, settings_hostname)

    def test_basesetting_gethostname_hostname_supplied(self):
        expected_hostname = 'test here'
        settings_hostname = BaseSetting._get_hostname(system_specific=False, hostname=expected_hostname)
        self.assertEqual(expected_hostname, settings_hostname)

    @override_settings(
        IARPDJANGOUTILS_SETTINGS_USE_HOSTNAME_SEPARATION=False
    )
    def test_basesetting_gethostname_settings_deny_hostname_use(self):
        expected_hostname = ''
        settings_hostname = BaseSetting._get_hostname(system_specific=False, hostname=expected_hostname)
        self.assertEqual(expected_hostname, settings_hostname)

        settings_hostname = BaseSetting._get_hostname(system_specific=True)
        self.assertEqual(expected_hostname, settings_hostname)

        settings_hostname = BaseSetting._get_hostname()
        self.assertEqual(expected_hostname, settings_hostname)
