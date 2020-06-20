from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from iarp_django_utils.helpers import only_save_changed_data, get_name_name_for_queryset_filter, get_app_name_for_queryset_filter


class HelperTests(TestCase):

    def setUp(self) -> None:
        self.obj = self.create_test_obj()

    def create_test_obj(self):
        class TestObj:
            first_name = 'John'
            last_name = 'Doe'
            inserted = timezone.now() - timezone.timedelta(hours=1)

            test_field1 = 'field1'
            test_field2 = 'field2'

            def save(self, *args, **kwargs):
                pass

        return TestObj()

    def test_only_save_changed_data_with_changed_data(self):

        obj_data = {
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
        output = only_save_changed_data(self.obj, obj_data)
        self.assertEqual(1, len(output))
        self.assertIn('first_name', output)

    def test_only_save_changed_data_with_not_fields(self):

        obj_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'inserted': timezone.now(),
        }
        output = only_save_changed_data(self.obj, obj_data, not_these_fields=['inserted'])
        self.assertEqual(1, len(output))
        self.assertIn('first_name', output)

    def test_only_save_changed_data_with_not_fields_startswith(self):

        obj_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'test_field1': 'field3',
            'test_field2': 'field4'
        }
        output = only_save_changed_data(self.obj, obj_data, not_these_fields_startswith=['test_'])
        self.assertEqual(1, len(output))
        self.assertIn('first_name', output)

        self.obj = self.create_test_obj()

        output = only_save_changed_data(self.obj, obj_data, not_these_fields_startswith=['tests_'])
        self.assertEqual(3, len(output))
        self.assertIn('first_name', output)
        self.assertIn('test_field1', output)
        self.assertIn('test_field2', output)

    def test_only_save_changed_data_raises_type_errors(self):
        with self.assertRaises(TypeError):
            only_save_changed_data(self.obj, {}, not_these_fields={}.items())
        with self.assertRaises(TypeError):
            only_save_changed_data(self.obj, {}, not_these_fields_startswith={}.items())

    def test_app_name_queryset_filter_returns_case_sensitive(self):
        val = get_app_name_for_queryset_filter()
        self.assertEqual('app', val)

    @override_settings(IARPDJANGOUTILS_SETTINGS_CASE_SENSITIVE_APP=False)
    def test_app_name_queryset_filter_returns_case_insensitive(self):
        val = get_app_name_for_queryset_filter()
        self.assertEqual('app__iexact', val)

    def test_name_name_queryset_filter_returns_case_sensitive(self):
        val = get_name_name_for_queryset_filter()
        self.assertEqual('name', val)

    @override_settings(IARPDJANGOUTILS_SETTINGS_CASE_SENSITIVE_NAME=False)
    def test_name_name_queryset_filter_returns_case_insensitive(self):
        val = get_name_name_for_queryset_filter()
        self.assertEqual('name__iexact', val)
