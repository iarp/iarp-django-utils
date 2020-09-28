from django import template
from django.contrib.auth.models import User


register = template.Library()


@register.simple_tag(takes_context=True)
def get_hijacker(context):
    """ django-hijack allows you to login as another
        user while still being logged in as yourself.

        This returns the user that is doing the hijacking of another user.
    """
    try:
        user_id = context['request'].session['hijack_history'][0]

        return User.objects.get(pk=user_id)

    except (KeyError, IndexError, User.DoesNotExist, TypeError):
        return False
