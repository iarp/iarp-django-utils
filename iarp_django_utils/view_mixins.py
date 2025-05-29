from django.conf import settings
from django.shortcuts import redirect


class RestrictQuerySetToAuthorizedUserMixin:

    queryset_restrict_user_field = "user"

    def get_queryset(self):
        return super().get_queryset().filter(**{self.queryset_restrict_user_field: self.request.user})


class UserIsStaffOrAbove:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request=request, *args, **kwargs)


class NextOrSuccessUrlRedirectionMixin:
    def get_next_url(self):
        next_ = self.request.GET.get("next")
        if next_:
            next_ = next_.split("#", 1)[0]
            return next_

    def get_success_url(self):
        next_ = self.get_next_url()
        if next_:
            return next_
        return super().get_success_url()
