from django.core.paginator import Paginator
from django.test import RequestFactory, TestCase

from iarp_django_utils.pagination import paginator_helper
from iarp_django_utils.templatetags import proper_pagination

from .models import TestModel


class TemplateTagsProperPaginationTests(TestCase):

    def setUp(self) -> None:
        for x in range(100):
            TestModel.objects.create(name=x)

    def test_default_pagination_settings_with_low_number_of_pages(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 10),
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], output)

    def test_default_pagination_settings_with_high_number_of_pages(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            current_page=8
        )
        self.assertEqual([4, 5, 6, 7, 8, 9, 10, 11, 12], output)

    def test_default_pagination_settings_with_large_neighbors(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            current_page=15,
            neighbors=10
        )
        self.assertEqual([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], output)

    def test_proper_pagination_settings_with_first(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            current_page=12,
            include_first=2,
        )
        self.assertEqual([1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16], output)

    def test_proper_pagination_settings_with_last(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            current_page=12,
            include_last=2,
        )
        self.assertEqual([8, 9, 10, 11, 12, 13, 14, 15, 16, 49, 50], output)

    def test_proper_pagination_settings_with_first_and_last(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            current_page=12,
            include_first=2,
            include_last=2,
        )
        self.assertEqual([1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 49, 50], output)

    def test_proper_pagination_settings_with_first_and_last_and_separator(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            current_page=12,
            include_first=2,
            include_last=2,
            include_separator='...'
        )
        self.assertEqual([1, 2, '...', 8, 9, 10, 11, 12, 13, 14, 15, 16, '...', 49, 50], output)

    def test_proper_pagination_settings_with_first_last_separator_and_small_neighbors(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            neighbors=2,
            current_page=12,
            include_first=2,
            include_last=2,
            include_separator='...'
        )
        self.assertEqual([1, 2, '...', 10, 11, 12, 13, 14, '...', 49, 50], output)

    def test_proper_pagination_settings_with_first_last_separator_and_large_neighbors(self):
        output = proper_pagination.proper_pagination(
            paginator=Paginator(TestModel.objects.all().order_by('id'), 2),
            neighbors=10,
            current_page=12,
            include_first=2,
            include_last=2,
            include_separator='...'
        )
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                          14, 15, 16, 17, 18, 19, 20, 21, 22, '...', 49, 50], output)


class PaginationHelperTests(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

        for x in range(100):
            TestModel.objects.create(name=x)

    def test_base_pagination_settings(self):

        context_key = 'object_list_key'
        output = paginator_helper(
            context_key=context_key,
            queryset=TestModel.objects.all().order_by('id'),
            requested_page=1,
            limit=2,
        )

        self.assertIn(context_key, output)
        self.assertEqual(2, output[context_key].count())
        self.assertTrue(output['is_paginated'])
        self.assertEqual('?', output['pagination_base_url'])
        self.assertEqual(1, output['page_obj'].number)

    def test_pagination_with_params(self):

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            params={
                'page': 1,
                'limit': 2,
                'search': 'search text'
            }
        )

        self.assertEqual('?limit=2&search=search+text&', output['pagination_base_url'])

    def test_pagination_requested_page_too_high(self):

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            requested_page=100,
        )
        self.assertEqual(7, output['page_obj'].number)

    def test_pagination_requested_page_too_low(self):

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            requested_page=-2,
        )
        self.assertEqual(1, output['page_obj'].number)

    def test_pagination_requested_page_is_invalid(self):

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            requested_page='2nd',
        )
        self.assertEqual(1, output['page_obj'].number)

    def test_pagination_custom_limit_url_param(self):

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            limit=2,
            limit_url_param='limiter',
            params={
                'limiter': 15
            }
        )
        self.assertEqual(7, output['paginator'].num_pages)

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            limit=2,
            limit_url_param='limiter',
            params={
                'limiter': 30
            }
        )
        self.assertEqual(4, output['paginator'].num_pages)

    def test_pagination_custom_page_url_param(self):

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            page_url_param='page_id',
            limit=3,
            params={
                'page_id': 15
            }
        )
        self.assertEqual(15, output['page_obj'].number)

        output = paginator_helper(
            context_key='objects',
            queryset=TestModel.objects.all().order_by('id'),
            page_url_param='page_id',
            limit=2,
            params={
                'page_id': 15
            }
        )
        self.assertEqual(15, output['page_obj'].number)

    def test_pagination_last_first_true(self):

        output = paginator_helper(
            context_key='object_list_key',
            queryset=TestModel.objects.all().order_by('id'),
            limit=2,
            last_first=True
        )
        self.assertEqual(50, output['page_obj'].number)

        output = paginator_helper(
            context_key='object_list_key',
            queryset=TestModel.objects.all().order_by('id'),
            limit=2,
            requested_page=7,
            last_first=True
        )
        self.assertEqual(7, output['page_obj'].number)
