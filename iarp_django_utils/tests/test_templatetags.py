from django.template import RequestContext
from django.test import RequestFactory, TestCase

from iarp_django_utils.templatetags import request_tools


class RequestToolsTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_posted_or_default_expecting_default(self):
        request = self.factory.post('/')
        context = RequestContext(request)
        data = request_tools.posted_or_default(context, 'test', 'default')
        self.assertEqual('default', data)

    def test_posted_or_default_with_posted_data(self):
        request = self.factory.post('/', {'test': 'data in here'})
        context = RequestContext(request)
        data = request_tools.posted_or_default(context, 'test', 'default data')
        self.assertEqual('data in here', data)

    def test_posted_or_not_posted_posted_but_not_exists(self):
        request = self.factory.post('/', {'test': 'data in here'})
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '123', 'selected')
        self.assertEqual(data, '')

    def test_posted_or_not_posted_posted_and_exists(self):
        request = self.factory.post('/', {'test': 'true'})
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '123', 'selected')
        self.assertEqual(data, 'selected')

    def test_posted_or_not_posted_posted_as_get_and_exists(self):
        request = self.factory.get('/')
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '123', 'selected')
        self.assertEqual(data, 'selected')

    def test_posted_or_not_posted_posted_as_get_and_not_exists(self):
        request = self.factory.get('/')
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '231', 'selected')
        self.assertEqual(data, '')

    def test_build_url_with_existing_params(self):
        request = self.factory.get('/?test=here')
        context = {'request': request}

        output = request_tools.build_url_with_existing_params(context, page=2)
        expected = '/?test=here&page=2'
        self.assertEqual(expected, output)

    def test_build_url_with_existing_params_alters_existing_param(self):
        request = self.factory.get('/?test=here')
        context = {'request': request}

        output = request_tools.build_url_with_existing_params(context, page=2, test='blah')
        expected = '/?test=blah&page=2'
        self.assertEqual(expected, output)
