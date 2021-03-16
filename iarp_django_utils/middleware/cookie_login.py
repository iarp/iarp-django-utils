from django.conf import settings
from django.contrib.auth import get_user_model, login

from iarp_utils.system import import_callable


User = get_user_model()


def auth_check(user, cookie_value, request):
    return user.check_cookie_password(cookie_value)


class CookieAutoLogin(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        system_auth_checker = getattr(settings, "COOKIE_LOGIN_AUTH", None)
        if system_auth_checker:
            system_auth_checker = import_callable(system_auth_checker)
        else:
            system_auth_checker = auth_check

        cookie_key = getattr(settings, "COOKIE_LOGIN_KEY", None)

        if not cookie_key:
            raise ValueError("CookieAutoLogin requires COOKIE_LOGIN_KEY in settings.")

        if cookie_key in request.COOKIES and not request.user.is_authenticated:
            cookie_value = request.COOKIES[cookie_key]
            for user in User.objects.filter(cookie_password__isnull=False):
                output = system_auth_checker(user=user, cookie_value=cookie_value, request=request)
                if output:
                    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                break

        return self.get_response(request)
