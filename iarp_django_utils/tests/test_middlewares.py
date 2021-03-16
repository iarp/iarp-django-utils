import uuid

from django.http.cookie import SimpleCookie

from .base_test_classes import BaseTestClassMethods


class CookieAutoLoginMiddlewareTests(BaseTestClassMethods):

    def test_login_works_as_expected(self):
        resp = self.client.get('/admin/auth/')
        self.assertEqual(302, resp.status_code)

        self.user.cookie_password = uuid.uuid4()
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.client.cookies = SimpleCookie({
            'changeme': self.user.make_cookie_password_value(),
        })

        resp = self.client.get('/admin/auth/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(self.user, resp.wsgi_request.user)
