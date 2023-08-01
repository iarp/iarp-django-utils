import socket

from django.test.utils import override_settings
from django.template import Template, Context

from .base_test_classes import BaseTestClassMethods
from .models import PageContent


class PageContentsTests(BaseTestClassMethods):

    def test_page_contents_blank_on_new(self):
        template = Template("{% load page_contents %}{% page_contents 'core' 'index' False %}")
        output = template.render(Context())
        self.assertEqual('', output)

        pages_count = PageContent.objects.all().count()
        self.assertEqual(1, pages_count)

        entry = PageContent.objects.get()
        self.assertEqual('core', entry.app)
        self.assertEqual('index', entry.location)
        self.assertEqual('', entry.contents)

    def test_page_contents_creates_single_entry(self):
        template = Template("{% load page_contents %}{% page_contents 'core' 'index' False %}")
        template.render(Context())
        template = Template("{% load page_contents %}{% page_contents 'core' 'index' False %}")
        template.render(Context())

        pages_count = PageContent.objects.all().count()
        self.assertEqual(1, pages_count)

    def test_page_contents_shows_div_wrapper_with_param_supplied(self):
        template = Template("{% load page_contents %}{% page_contents 'core' 'index' True %}")
        output = template.render(Context())

        pc = PageContent.objects.get()

        expected = f"""
        <div class="page-contents-wrapper {pc.location}" data-page-contents-id="{pc.id}">
            <div class="page-contents-contents">
                {pc.contents}
            </div>
        </div>"""
        self.assertEqual(expected, output)

    def test_page_contents_shows_div_wrapper_without_param_supplied(self):
        template = Template("{% load page_contents %}{% page_contents 'core' 'index' %}")
        output = template.render(Context())

        pc = PageContent.objects.get()

        expected = f"""
        <div class="page-contents-wrapper {pc.location}" data-page-contents-id="{pc.id}">
            <div class="page-contents-contents">
                {pc.contents}
            </div>
        </div>"""
        self.assertEqual(expected, output)

    def test_page_contents_shows_attributed_request_data(self):

        pc, _ = PageContent.objects.update_or_create(app='core', location='index', contents='{{user.username}}')

        class Request:
            user = self.user
        req = Request()

        template = Template("{% load page_contents %}{% page_contents 'core' 'index' %}")
        output = template.render(Context({'request': req}))

        expected = f"""
        <div class="page-contents-wrapper {pc.location}" data-page-contents-id="{pc.id}">
            <div class="page-contents-contents">
                test
            </div>
        </div>"""
        self.assertEqual(expected, output)
