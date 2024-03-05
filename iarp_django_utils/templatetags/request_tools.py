from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def posted_or_default(context, name, default='', prepend_name='', *args, **kwargs):
    """
    Returns the posted value if it exists, otherwise returns default
    """
    if prepend_name:
        name = f'{prepend_name}_{name}'
    return context.request.POST.get(name, default)


@register.simple_tag(takes_context=True)
def only_when_posted(context, name, value, ret_val, prepend_name='', *args, **kwargs):
    """
    Only returns ret_val when request.method == POST otherwise blank

    Usage: ``{% "Played" "yes" "selected" player_id %}``

    Identical to  ``{% if request.method == 'POST' and request.POST['<player_id>_Played'] == "yes" %}selected{%endif%}``
    even though this doesn't work in templates as is.

    Args:
        :name: element Name
        :value: value to compare against
        :ret_val: Value to return if posted value equals value
        :prepend_name: Value to prepend onto name with an underscore i.e a player id 12412_Goals
    """
    if prepend_name:
        name = f'{prepend_name}_{name}'
    if isinstance(value, int):
        value = str(value)
    return ret_val if context.request.method == 'POST' and context.request.POST.get(name) == value else ''


@register.simple_tag(takes_context=True)
def posted_or_not_posted(context, posted_name, posted_value, cval1, cval2, ret_val, prepend_name='', *args, **kwargs):
    """Compares 2 values if request.method == 'POST' otherwise it compares cval1 and cval2

    This was mainly developed for use with hard-coded select elements.

    Examples:

        {% posted_or_not_posted "Game_Played" "no" game_data.Played 0 "selected" %}
        - What that breaks down into is:

        if request.method == 'POST':
            if request.POST['Game_Played'] == 'no':
                return 'selected'
            return ''
        if game_data.Played == 0:
            return 'selected'
        return ''
    """

    if prepend_name:
        posted_name = f'{prepend_name}_{posted_name}'

    try:
        posted_value = int(posted_value)
    except ValueError:
        pass

    if context.request.method == 'POST':
        pv = context.request.POST.get(posted_name)
        try:
            pv = int(pv)
        except ValueError:
            pass
        return ret_val if pv == posted_value else ''

    try:
        cval1 = int(cval1)
    except ValueError:
        pass

    try:
        cval2 = int(cval2)
    except ValueError:
        pass

    return ret_val if cval1 == cval2 else ''


@register.simple_tag(takes_context=True)
def build_url_with_existing_params(context, not_these=None, **kwargs):
    """
        Builds a url with existing parameters.

        not_these should be a comma separated list of keys to replace within the url

        {% if request.GET.o == '-inserted' %}
            {% build_url_with_existing_params o='inserted' %}
        {% elif request.GET.o == 'inserted' %}
            {% build_url_with_existing_params 'o' %}
        {% else %}
            {% build_url_with_existing_params o='-inserted' %}
        {% endif %}

        http://127.0.0.1:8000/?year=2007&missing=True&o=downloaded

        The above will cause the above url to swap o= on the url
    """
    if not_these:
        not_these = not_these.split(',')
    request = context['request']
    params = request.GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    if not_these:
        for k in not_these:
            params.pop(k, None)
    return f"{request.path}?{params.urlencode()}"
