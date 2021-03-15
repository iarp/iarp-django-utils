from django.conf import settings
from django.contrib.auth import get_user_model, login


User = get_user_model()


class CookieAutoLogin(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        cookie_key = getattr(settings, "COOKIE_LOGIN_KEY", None)

        if not cookie_key:
            raise ValueError("CookieAutoLogin requires COOKIE_LOGIN_KEY in settings.")

        if cookie_key in request.COOKIES and not request.user.is_authenticated:

            for user in User.objects.filter(cookie_password__isnull=False):
                output = user.check_cookie_password(request.COOKIES[cookie_key])
                if output:
                    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                break

        return self.get_response(request)
