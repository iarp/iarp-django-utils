import socket

from django.test.utils import override_settings

from iarp_django_utils.models import BaseSetting
from iarp_django_utils.tests.models import Setting

from .base_test_classes import BaseTestClassMethods


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

    @override_settings(IARPDJANGOUTILS_SETTINGS_USE_HOSTNAME_SEPARATION=False)
    def test_basesetting_gethostname_settings_deny_hostname_use(self):
        expected_hostname = ''
        settings_hostname = BaseSetting._get_hostname(system_specific=False, hostname=expected_hostname)
        self.assertEqual(expected_hostname, settings_hostname)

        settings_hostname = BaseSetting._get_hostname(system_specific=True)
        self.assertEqual(expected_hostname, settings_hostname)

        settings_hostname = BaseSetting._get_hostname()
        self.assertEqual(expected_hostname, settings_hostname)


class SettingsModelTests(BaseTestClassMethods):
    def test_basic_set_value_test(self):
        s = Setting.set_value('tests.name', value='here in tests')
        self.assertEqual('here in tests', s.value)
        self.assertEqual('tests', s.app)
        self.assertEqual('name', s.name)

    def test_basic_get_value_test(self):
        expected_value = 'here in tests'
        Setting.set_value('tests.name2', value=expected_value)
        returned_value = Setting.get_value('tests.name2')
        self.assertEqual(expected_value, returned_value)

    @override_settings(IARPDJANGOUTILS_SETTINGS_CASE_SENSITIVE_APP=False)
    def test_case_insensitive_app_get_value(self):
        expected_value = 'here in tests'
        Setting.set_value('tests.name2', value=expected_value)
        returned_value = Setting.get_value('TESTS.name2')
        self.assertEqual(expected_value, returned_value)
        returned_value = Setting.get_value('tests.name2')
        self.assertEqual(expected_value, returned_value)

    @override_settings(IARPDJANGOUTILS_SETTINGS_CASE_SENSITIVE_APP=True)
    def test_case_sensitive_app_get_value(self):
        expected_value = 'here in tests'
        Setting.set_value('tests.name2', value=expected_value)
        returned_value = Setting.get_value('TESTS.name2')
        self.assertEqual('', returned_value)
        returned_value = Setting.get_value('tests.name2')
        self.assertEqual(expected_value, returned_value)

    @override_settings(IARPDJANGOUTILS_SETTINGS_CASE_SENSITIVE_NAME=False)
    def test_case_sensitive_name_get_value(self):
        expected_value = 'here in tests'
        Setting.set_value('tests.name2', value=expected_value)
        returned_value = Setting.get_value('tests.NAME2')
        self.assertEqual(expected_value, returned_value)
        returned_value = Setting.get_value('tests.name2')
        self.assertEqual(expected_value, returned_value)

    @override_settings(IARPDJANGOUTILS_SETTINGS_CASE_SENSITIVE_NAME=True)
    def test_case_insensitive_name_get_value(self):
        expected_value = 'here in tests'
        Setting.set_value('tests.name2', value=expected_value)
        returned_value = Setting.get_value('tests.NAME2')
        self.assertEqual('', returned_value)
        returned_value = Setting.get_value('tests.name2')
        self.assertEqual(expected_value, returned_value)
