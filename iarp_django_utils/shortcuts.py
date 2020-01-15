from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def redirect_next_or_obj(request, other, next_key='next'):
    """ Default redirect to given object, if next_key
        in request.GET then redirect there instead.
    """
    next_param = getattr(request, 'GET', {}).get(next_key)
    if next_param:
        return HttpResponseRedirect(next_param)
    return redirect(other)
