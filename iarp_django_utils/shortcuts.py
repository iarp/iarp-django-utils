from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def redirect_next_or_obj(request, other, next_key="next"):
    """Default redirect to given object, if next_key
    in request.GET then redirect there instead.
    """
    next_param = getattr(request, "GET", {}).get(next_key)
    if next_param:
        return HttpResponseRedirect(next_param)
    return redirect(other)


def redirect_next_or_obj_as_str(request, other):
    next_param = getattr(request, "GET", {}).get("next")
    if next_param:
        return next_param
    if hasattr(other, "get_absolute_url"):
        other = other.get_absolute_url()
    return other
