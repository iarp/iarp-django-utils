import pathlib

from unittest.mock import call, patch

from django.core.files.base import ContentFile
from django.core.files.storage import InMemoryStorage
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from iarp_django_utils.helpers import (
    delete_tree_using_storage,
    get_app_name_for_queryset_filter,
    get_name_name_for_queryset_filter,
    only_save_changed_data,
)


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

        obj_data = {'first_name': 'Jane', 'last_name': 'Doe'}
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

        obj_data = {'first_name': 'Jane', 'last_name': 'Doe', 'test_field1': 'field3', 'test_field2': 'field4'}
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

    @patch("django.core.files.storage.InMemoryStorage.delete")
    def test_delete_tree_using_storage_returns_when_directory_does_not_exist(self, mock_delete):
        storage = InMemoryStorage()

        path = pathlib.Path("cache/inmem/")

        delete_tree_using_storage(
            path=path,
            delete_root=True,
            storage=storage,
        )

        mock_delete.assert_not_called()

    @patch("django.core.files.storage.InMemoryStorage.delete")
    def test_delete_tree_using_storage_deletes_file_and_root(self, mock_delete):
        storage = InMemoryStorage()

        path = pathlib.Path("cache/inmem")

        storage.save(path / "touched", ContentFile("test"))
        storage.save(path / "touched2", ContentFile("test"))

        delete_tree_using_storage(
            path=path,
            delete_root=True,
            storage=storage,
        )

        mock_delete.assert_has_calls([
            call(path / "touched"),
            call(path / "touched2"),
            call(path),
        ])

    @patch("django.core.files.storage.InMemoryStorage.delete")
    def test_delete_tree_using_storage_deletes_file_and_keeps_root(self, mock_delete):
        storage = InMemoryStorage()

        path = pathlib.Path("cache/inmem")

        storage.save(path / "touched", ContentFile("test"))

        delete_tree_using_storage(
            path=path,
            storage=storage,
        )

        mock_delete.assert_called_once_with(path / "touched")
